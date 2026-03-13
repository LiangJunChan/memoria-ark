from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Achievement, DigitalAsset, SystemConfig
from app import db
from sqlalchemy import desc
achievement_bp = Blueprint('achievement', __name__)
# 获取用户成就数据
@achievement_bp.route('/data', methods=['GET'])
@jwt_required()
def get_achievement_data():
    user_id = get_jwt_identity()
    achievement = Achievement.query.filter_by(user_id=user_id).first()
    
    if not achievement:
        achievement = Achievement(user_id=user_id)
        db.session.add(achievement)
        db.session.commit()
    
    # 检查勋章
    medals = check_medals(user_id, achievement)
    achievement.medals = medals
    db.session.commit()
    
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': achievement.to_dict()
    })
# 检查勋章解锁情况
def check_medals(user_id, achievement):
    medal_config = SystemConfig.get_config('medals') or []
    unlocked_medals = achievement.medals or []
    unlocked_ids = [medal.get('id') for medal in unlocked_medals]
    
    total_assets = achievement.total_assets
    total_carbon = float(achievement.total_carbon_reduction)
    
    for medal in medal_config:
        medal_id = medal.get('id')
        if medal_id in unlocked_ids:
            continue
            
        condition = medal.get('condition', '')
        unlocked = False
        
        # 解析条件
        if condition.startswith('创建第一个数字资产'):
            unlocked = total_assets >= 1
        elif condition.startswith('累计10件资产'):
            unlocked = total_assets >= 10
        elif condition.startswith('累计50件资产'):
            unlocked = total_assets >= 50
        elif condition.startswith('累计碳减量100kg'):
            unlocked = total_carbon >= 100
        elif condition.startswith('累计碳减量500kg'):
            unlocked = total_carbon >= 500
        
        if unlocked:
            unlocked_medals.append({
                'id': medal_id,
                'name': medal.get('name'),
                'icon': medal.get('icon'),
                'unlock_time': db.func.now().isoformat()
            })
    
    return unlocked_medals
# 获取排行榜
@achievement_bp.route('/rank', methods=['GET'])
@jwt_required()
def get_rank():
    user_id = get_jwt_identity()
    type = request.args.get('type', 'carbon')  # carbon: 碳积分, assets: 资产数
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    
    query = Achievement.query
    
    if type == 'carbon':
        query = query.order_by(desc(Achievement.total_carbon_reduction))
    else:
        query = query.order_by(desc(Achievement.total_assets))
    
    pagination = query.paginate(page=page, per_page=page_size, error_out=False)
    
    # 计算排名
    rank_list = []
    current_rank = (page - 1) * page_size + 1
    
    for achievement in pagination.items:
        user = achievement.user
        if not user:
            continue
            
        rank_data = {
            'rank': current_rank,
            'user_id': user.id,
            'username': user.username,
            'avatar': user.avatar,
            'total_assets': achievement.total_assets,
            'total_carbon_reduction': float(achievement.total_carbon_reduction)
        }
        rank_list.append(rank_data)
        current_rank += 1
    
    # 获取当前用户排名
    user_achievement = Achievement.query.filter_by(user_id=user_id).first()
    user_rank = None
    
    if user_achievement:
        if type == 'carbon':
            count = Achievement.query.filter(Achievement.total_carbon_reduction > user_achievement.total_carbon_reduction).count()
        else:
            count = Achievement.query.filter(Achievement.total_assets > user_achievement.total_assets).count()
        user_rank = count + 1
    
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': {
            'list': rank_list,
            'total': pagination.total,
            'page': page,
            'page_size': page_size,
            'total_pages': pagination.pages,
            'user_rank': user_rank,
            'user_data': user_achievement.to_dict() if user_achievement else None
        }
    })
# 获取统计数据
@achievement_bp.route('/statistics', methods=['GET'])
@jwt_required()
def get_statistics():
    user_id = get_jwt_identity()
    
    # 用户数据
    achievement = Achievement.query.filter_by(user_id=user_id).first()
    if not achievement:
        achievement = Achievement(user_id=user_id)
        db.session.add(achievement)
        db.session.commit()
    
    # 分类统计
    category_stats = db.session.query(
        DigitalAsset.category,
        db.func.count(DigitalAsset.id).label('count'),
        db.func.sum(DigitalAsset.carbon_reduction).label('carbon')
    ).filter_by(user_id=user_id).group_by(DigitalAsset.category).all()
    
    category_data = []
    for stat in category_stats:
        category_data.append({
            'category': stat.category,
            'count': stat.count,
            'carbon_reduction': float(stat.carbon or 0)
        })
    
    # 最近7天数据
    seven_days_ago = db.func.date_sub(db.func.now(), db.text('INTERVAL 7 DAY'))
    daily_stats = db.session.query(
        db.func.date(DigitalAsset.created_at).label('date'),
        db.func.count(DigitalAsset.id).label('count'),
        db.func.sum(DigitalAsset.carbon_reduction).label('carbon')
    ).filter_by(user_id=user_id).filter(DigitalAsset.created_at >= seven_days_ago)\
     .group_by(db.func.date(DigitalAsset.created_at)).order_by('date').all()
    
    daily_data = []
    for stat in daily_stats:
        daily_data.append({
            'date': str(stat.date),
            'count': stat.count,
            'carbon_reduction': float(stat.carbon or 0)
        })
    
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': {
            'total_assets': achievement.total_assets,
            'total_carbon_reduction': float(achievement.total_carbon_reduction),
            'medals_count': len(achievement.medals or []),
            'category_stats': category_data,
            'daily_stats': daily_data
        }
    })
# 手动触发勋章检查
@achievement_bp.route('/check-medals', methods=['POST'])
@jwt_required()
def check_medals_api():
    user_id = get_jwt_identity()
    achievement = Achievement.query.filter_by(user_id=user_id).first()
    
    if not achievement:
        return jsonify({'code': 404, 'message': '用户成就数据不存在', 'data': None}), 404
    
    medals = check_medals(user_id, achievement)
    new_medals = []
    
    # 找出新解锁的勋章
    old_medal_ids = [m.get('id') for m in (achievement.medals or [])]
    for medal in medals:
        if medal.get('id') not in old_medal_ids:
            new_medals.append(medal)
    
    achievement.medals = medals
    db.session.commit()
    
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': {
            'all_medals': medals,
            'new_medals': new_medals
        }
    })

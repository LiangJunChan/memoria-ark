from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import UserSpace, AICompanion, SystemConfig
from app import db
import json
space_bp = Blueprint('space', __name__)
# 获取用户空间配置
@space_bp.route('/config', methods=['GET'])
@jwt_required()
def get_space_config():
    user_id = get_jwt_identity()
    space = UserSpace.query.filter_by(user_id=user_id).first()
    
    if not space:
        return jsonify({
            'code': 0,
            'message': 'success',
            'data': None
        })
    
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': space.to_dict()
    })
# 创建/更新空间配置
@space_bp.route('/config', methods=['POST'])
@jwt_required()
def save_space_config():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    required_fields = ['style', 'size', 'floor_count', 'has_yard', 'room_count', 'layout_config', 'furniture_config']
    for field in required_fields:
        if field not in data:
            return jsonify({'code': 400, 'message': f'缺少必填参数：{field}', 'data': None}), 400
    
    # 检查是否已存在空间配置
    space = UserSpace.query.filter_by(user_id=user_id).first()
    
    try:
        if space:
            # 更新
            space.style = data['style']
            space.size = data['size']
            space.floor_count = data['floor_count']
            space.has_yard = data['has_yard']
            space.room_count = data['room_count']
            space.layout_config = data['layout_config']
            space.furniture_config = data['furniture_config']
            space.preview_image = data.get('preview_image')
        else:
            # 新建
            space = UserSpace(
                user_id=user_id,
                style=data['style'],
                size=data['size'],
                floor_count=data['floor_count'],
                has_yard=data['has_yard'],
                room_count=data['room_count'],
                layout_config=data['layout_config'],
                furniture_config=data['furniture_config'],
                preview_image=data.get('preview_image')
            )
            db.session.add(space)
        
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'message': '空间配置保存成功',
            'data': space.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'保存失败：{str(e)}', 'data': None}), 500
# 获取AI伴侣信息
@space_bp.route('/ai-companion', methods=['GET'])
@jwt_required()
def get_ai_companion():
    user_id = get_jwt_identity()
    ai = AICompanion.query.filter_by(user_id=user_id).first()
    
    if not ai:
        return jsonify({
            'code': 0,
            'message': 'success',
            'data': None
        })
    
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': ai.to_dict()
    })
# 保存AI伴侣配置
@space_bp.route('/ai-companion', methods=['POST'])
@jwt_required()
def save_ai_companion():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if 'name' not in data or 'avatar' not in data:
        return jsonify({'code': 400, 'message': '缺少必填参数：name或avatar', 'data': None}), 400
    
    ai = AICompanion.query.filter_by(user_id=user_id).first()
    
    try:
        if ai:
            ai.name = data['name']
            ai.avatar = data['avatar']
            ai.personality = data.get('personality', 'warm')
        else:
            ai = AICompanion(
                user_id=user_id,
                name=data['name'],
                avatar=data['avatar'],
                personality=data.get('personality', 'warm')
            )
            db.session.add(ai)
        
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'message': 'AI伴侣配置保存成功',
            'data': ai.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'保存失败：{str(e)}', 'data': None}), 500
# 获取空间默认配置
@space_bp.route('/default-config', methods=['GET'])
def get_default_config():
    style = request.args.get('style', 'loft')
    styles = SystemConfig.get_config('space_styles') or []
    
    default_config = None
    for s in styles:
        if s.get('key') == style:
            default_config = {
                'size': 100,
                'floor_count': s.get('default_floor', 1),
                'has_yard': 0,
                'room_count': s.get('default_room', 3),
                'layout_config': {
                    'rooms': [
                        {'id': 1, 'name': '客厅', 'type': 'living', 'area': 30},
                        {'id': 2, 'name': '卧室', 'type': 'bedroom', 'area': 20},
                        {'id': 3, 'name': '书房', 'type': 'study', 'area': 15}
                    ]
                },
                'furniture_config': {
                    'living': ['沙发', '茶几', '电视柜'],
                    'bedroom': ['床', '衣柜', '床头柜'],
                    'study': ['书桌', '书架', '椅子']
                }
            }
            break
    
    if not default_config:
        default_config = {
            'size': 100,
            'floor_count': 1,
            'has_yard': 0,
            'room_count': 3,
            'layout_config': {'rooms': []},
            'furniture_config': {}
        }
    
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': default_config
    })

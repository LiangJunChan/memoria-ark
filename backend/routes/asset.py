from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import DigitalAsset, Achievement, SystemConfig
from app import db
import uuid
import os
from werkzeug.utils import secure_filename
import json
asset_bp = Blueprint('asset', __name__)
# 允许上传的文件类型
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'glb', 'gltf', 'obj'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# 生成唯一资产ID
def generate_asset_id():
    return str(uuid.uuid4()).replace('-', '')
# 文件上传
@asset_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    user_id = get_jwt_identity()
    
    if 'file' not in request.files:
        return jsonify({'code': 400, 'message': '没有上传文件', 'data': None}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'code': 400, 'message': '未选择文件', 'data': None}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # 生成新的文件名
        ext = filename.rsplit('.', 1)[1].lower()
        new_filename = f"{uuid.uuid4().hex}.{ext}"
        
        # 确定保存目录
        if ext in {'png', 'jpg', 'jpeg', 'gif'}:
            save_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'images')
            file_type = 'image'
        else:
            save_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'models')
            file_type = 'model'
        
        os.makedirs(save_dir, exist_ok=True)
        file_path = os.path.join(save_dir, new_filename)
        file.save(file_path)
        
        # 返回访问URL
        server_url = os.getenv('SERVER_URL', 'http://localhost:5000')
        file_url = f"{server_url}/uploads/{file_type}/{new_filename}"
        
        return jsonify({
            'code': 0,
            'message': '上传成功',
            'data': {
                'url': file_url,
                'type': file_type,
                'filename': new_filename
            }
        })
    
    return jsonify({'code': 400, 'message': '不支持的文件类型', 'data': None}), 400
# 创建数字资产
@asset_bp.route('/create', methods=['POST'])
@jwt_required()
def create_asset():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    required_fields = ['name', 'category', 'cover_url', 'model_url']
    for field in required_fields:
        if field not in data:
            return jsonify({'code': 400, 'message': f'缺少必填参数：{field}', 'data': None}), 400
    
    # 计算碳减量
    carbon_config = SystemConfig.get_config('carbon_calculation') or {}
    carbon_reduction = carbon_config.get(data['category'], 1.0)
    
    # 生成资产ID
    asset_id = generate_asset_id()
    
    try:
        asset = DigitalAsset(
            user_id=user_id,
            asset_id=asset_id,
            name=data['name'],
            category=data['category'],
            description=data.get('description', ''),
            model_url=data['model_url'],
            cover_url=data['cover_url'],
            carbon_reduction=carbon_reduction,
            material=data.get('material'),
            position_config=data.get('position_config')
        )
        db.session.add(asset)
        
        # 更新成就数据
        achievement = Achievement.query.filter_by(user_id=user_id).first()
        if achievement:
            achievement.total_assets += 1
            achievement.total_carbon_reduction += carbon_reduction
        
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'message': '数字资产创建成功',
            'data': asset.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'创建失败：{str(e)}', 'data': None}), 500
# 获取资产列表
@asset_bp.route('/list', methods=['GET'])
@jwt_required()
def get_asset_list():
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    category = request.args.get('category')
    
    query = DigitalAsset.query.filter_by(user_id=user_id)
    
    if category:
        query = query.filter_by(category=category)
    
    pagination = query.order_by(DigitalAsset.created_at.desc()).paginate(page=page, per_page=page_size, error_out=False)
    
    assets = [asset.to_dict() for asset in pagination.items]
    
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': {
            'list': assets,
            'total': pagination.total,
            'page': page,
            'page_size': page_size,
            'total_pages': pagination.pages
        }
    })
# 获取资产详情
@asset_bp.route('/detail/<asset_id>', methods=['GET'])
@jwt_required()
def get_asset_detail(asset_id):
    user_id = get_jwt_identity()
    asset = DigitalAsset.query.filter_by(asset_id=asset_id, user_id=user_id).first()
    
    if not asset:
        return jsonify({'code': 404, 'message': '资产不存在', 'data': None}), 404
    
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': asset.to_dict()
    })
# 更新资产信息
@asset_bp.route('/update/<asset_id>', methods=['POST'])
@jwt_required()
def update_asset(asset_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    asset = DigitalAsset.query.filter_by(asset_id=asset_id, user_id=user_id).first()
    if not asset:
        return jsonify({'code': 404, 'message': '资产不存在', 'data': None}), 404
    
    try:
        if 'name' in data:
            asset.name = data['name']
        if 'category' in data:
            asset.category = data['category']
        if 'description' in data:
            asset.description = data['description']
        if 'cover_url' in data:
            asset.cover_url = data['cover_url']
        if 'model_url' in data:
            asset.model_url = data['model_url']
        if 'material' in data:
            asset.material = data['material']
        if 'position_config' in data:
            asset.position_config = data['position_config']
        
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'message': '更新成功',
            'data': asset.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'更新失败：{str(e)}', 'data': None}), 500
# 删除资产
@asset_bp.route('/delete/<asset_id>', methods=['POST'])
@jwt_required()
def delete_asset(asset_id):
    user_id = get_jwt_identity()
    
    asset = DigitalAsset.query.filter_by(asset_id=asset_id, user_id=user_id).first()
    if not asset:
        return jsonify({'code': 404, 'message': '资产不存在', 'data': None}), 404
    
    try:
        # 减去成就数据
        achievement = Achievement.query.filter_by(user_id=user_id).first()
        if achievement:
            achievement.total_assets -= 1
            achievement.total_carbon_reduction -= asset.carbon_reduction
            if achievement.total_assets < 0:
                achievement.total_assets = 0
            if achievement.total_carbon_reduction < 0:
                achievement.total_carbon_reduction = 0
        
        db.session.delete(asset)
        db.session.commit()
        
        return jsonify({
            'code': 0,
            'message': '删除成功',
            'data': None
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'删除失败：{str(e)}', 'data': None}), 500
# 获取分类列表
@asset_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    carbon_config = SystemConfig.get_config('carbon_calculation') or {}
    categories = list(carbon_config.keys())
    
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': categories
    })

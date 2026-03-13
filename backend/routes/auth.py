from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User, Achievement
from app import db
import hashlib
import re
auth_bp = Blueprint('auth', __name__)
# 密码加密
def encrypt_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()
# 注册
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # 参数校验
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'code': 400, 'message': '用户名和密码不能为空', 'data': None}), 400
    
    username = data['username'].strip()
    password = data['password'].strip()
    
    if len(username) < 3 or len(username) > 20:
        return jsonify({'code': 400, 'message': '用户名长度必须在3-20位之间', 'data': None}), 400
    
    if len(password) < 6 or len(password) > 32:
        return jsonify({'code': 400, 'message': '密码长度必须在6-32位之间', 'data': None}), 400
    
    # 检查用户名是否已存在
    if User.query.filter_by(username=username).first():
        return jsonify({'code': 400, 'message': '用户名已存在', 'data': None}), 400
    
    # 创建用户
    user = User(
        username=username,
        password=encrypt_password(password),
        phone=data.get('phone'),
        email=data.get('email')
    )
    
    try:
        db.session.add(user)
        db.session.flush()
        
        # 初始化成就表
        achievement = Achievement(user_id=user.id)
        db.session.add(achievement)
        
        db.session.commit()
        
        # 生成token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'code': 0,
            'message': '注册成功',
            'data': {
                'access_token': access_token,
                'user_info': user.to_dict()
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'注册失败：{str(e)}', 'data': None}), 500
# 登录
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'code': 400, 'message': '用户名和密码不能为空', 'data': None}), 400
    
    username = data['username'].strip()
    password = data['password'].strip()
    
    # 查询用户
    user = User.query.filter_by(username=username).first()
    
    if not user or user.password != encrypt_password(password):
        return jsonify({'code': 400, 'message': '用户名或密码错误', 'data': None}), 400
    
    if user.status != 1:
        return jsonify({'code': 403, 'message': '账号已被禁用', 'data': None}), 403
    
    # 生成token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'code': 0,
        'message': '登录成功',
        'data': {
            'access_token': access_token,
            'user_info': user.to_dict()
        }
    })
# 获取用户信息
@auth_bp.route('/info', methods=['GET'])
@jwt_required()
def get_user_info():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'code': 404, 'message': '用户不存在', 'data': None}), 404
    
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': user.to_dict()
    })
# 修改密码
@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or 'old_password' not in data or 'new_password' not in data:
        return jsonify({'code': 400, 'message': '参数错误', 'data': None}), 400
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'code': 404, 'message': '用户不存在', 'data': None}), 404
    
    if user.password != encrypt_password(data['old_password']):
        return jsonify({'code': 400, 'message': '原密码错误', 'data': None}), 400
    
    new_password = data['new_password'].strip()
    if len(new_password) < 6 or len(new_password) > 32:
        return jsonify({'code': 400, 'message': '新密码长度必须在6-32位之间', 'data': None}), 400
    
    try:
        user.password = encrypt_password(new_password)
        db.session.commit()
        return jsonify({'code': 0, 'message': '密码修改成功', 'data': None})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'message': f'修改失败：{str(e)}', 'data': None}), 500

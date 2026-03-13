from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import SystemConfig
import random
system_bp = Blueprint('system', __name__)
# 获取空间风格列表
@system_bp.route('/space-styles', methods=['GET'])
def get_space_styles():
    styles = SystemConfig.get_config('space_styles')
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': styles or []
    })
# 获取AI名称库
@system_bp.route('/ai-names', methods=['GET'])
def get_ai_names():
    names = SystemConfig.get_config('ai_names')
    # 随机返回10个名称
    if names and len(names) > 10:
        random_names = random.sample(names, 10)
    else:
        random_names = names or []
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': random_names
    })
# 获取AI头像库
@system_bp.route('/ai-avatars', methods=['GET'])
def get_ai_avatars():
    avatars = SystemConfig.get_config('ai_avatars')
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': avatars or []
    })
# 获取碳积分计算配置
@system_bp.route('/carbon-config', methods=['GET'])
def get_carbon_config():
    config = SystemConfig.get_config('carbon_calculation')
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': config or {}
    })
# 获取勋章配置
@system_bp.route('/medals', methods=['GET'])
def get_medals():
    medals = SystemConfig.get_config('medals')
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': medals or []
    })
# 随机生成AI配置
@system_bp.route('/random-ai', methods=['GET'])
def random_ai():
    names = SystemConfig.get_config('ai_names') or ['小忆', '阿存', '源']
    avatars = SystemConfig.get_config('ai_avatars') or ['/static/ai/default.png']
    personalities = ['warm', 'humorous', 'serious', 'cute']
    
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': {
            'name': random.choice(names),
            'avatar': random.choice(avatars),
            'personality': random.choice(personalities)
        }
    })
# 获取系统配置
@system_bp.route('/config', methods=['GET'])
def get_system_config():
    configs = SystemConfig.query.all()
    result = {}
    for config in configs:
        result[config.config_key] = config.config_value
    
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': result
    })

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from datetime import datetime, timedelta
import os
import json
import uuid
import hashlib
from dotenv import load_dotenv
# 加载环境变量
load_dotenv()
# 初始化Flask应用
app = Flask(__name__)
from urllib.parse import quote_plus

# 配置
db_user = os.getenv('MYSQL_USER')
db_password = quote_plus(os.getenv('MYSQL_PASSWORD'))  # 对密码进行URL编码，处理特殊字符
db_host = os.getenv('MYSQL_HOST')
db_port = os.getenv('MYSQL_PORT')
db_name = os.getenv('MYSQL_DB')

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?charset=utf8mb4"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES')))
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH'))
# 初始化扩展
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)
# 创建上传目录
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'images'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'models'), exist_ok=True)
# 导入模型
from models import User, UserSpace, AICompanion, DigitalAsset, Achievement, SystemConfig
# 注册蓝图
from routes.auth import auth_bp
from routes.system import system_bp
from routes.space import space_bp
from routes.asset import asset_bp
from routes.achievement import achievement_bp
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(system_bp, url_prefix='/api/system')
app.register_blueprint(space_bp, url_prefix='/api/space')
app.register_blueprint(asset_bp, url_prefix='/api/asset')
app.register_blueprint(achievement_bp, url_prefix='/api/achievement')
# 健康检查
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'code': 0,
        'message': 'success',
        'data': {
            'status': 'ok',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        }
    })
# 错误处理
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'code': 400, 'message': '请求参数错误', 'data': None}), 400
@app.errorhandler(401)
def unauthorized(error):
    return jsonify({'code': 401, 'message': '未授权访问', 'data': None}), 401
@app.errorhandler(403)
def forbidden(error):
    return jsonify({'code': 403, 'message': '禁止访问', 'data': None}), 403
@app.errorhandler(404)
def not_found(error):
    return jsonify({'code': 404, 'message': '资源不存在', 'data': None}), 404
@app.errorhandler(500)
def internal_error(error):
    return jsonify({'code': 500, 'message': '服务器内部错误', 'data': None}), 500
if __name__ == '__main__':
    app.run(host=os.getenv('HOST'), port=int(os.getenv('PORT')), debug=os.getenv('DEBUG') == 'True')

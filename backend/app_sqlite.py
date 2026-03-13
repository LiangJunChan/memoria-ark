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

# 配置SQLite数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///memoria_ark.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'default-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 604800)))
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', './uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))

# 初始化扩展
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

# 创建上传目录
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 用户模型
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

# 注册蓝图
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({'code': 400, 'message': 'Missing required fields'}), 400
    
    # 检查用户是否已存在
    if User.query.filter_by(username=username).first():
        return jsonify({'code': 400, 'message': 'Username already exists'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'code': 400, 'message': 'Email already exists'}), 400
    
    # 创建新用户
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    new_user = User(username=username, email=email, password_hash=password_hash)
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        'code': 200,
        'message': 'User registered successfully',
        'data': new_user.to_dict()
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'code': 400, 'message': 'Missing username or password'}), 400
    
    # 查找用户
    user = User.query.filter_by(username=username).first()
    
    if not user:
        return jsonify({'code': 401, 'message': 'Invalid username or password'}), 401
    
    # 验证密码
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    if password_hash != user.password_hash:
        return jsonify({'code': 401, 'message': 'Invalid username or password'}), 401
    
    # 生成JWT token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'code': 200,
        'message': 'Login successful',
        'data': {
            'token': access_token,
            'user': user.to_dict()
        }
    }), 200

@app.route('/api/system/status', methods=['GET'])
def system_status():
    return jsonify({
        'code': 200,
        'message': 'System is running',
        'data': {
            'status': 'online',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0'
        }
    }), 200

# 错误处理
@app.errorhandler(404)
def not_found(error):
    return jsonify({'code': 404, 'message': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'code': 500, 'message': 'Internal server error'}), 500

if __name__ == '__main__':
    # 创建数据库表
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
    
    # 启动Flask应用
    app.run(host='0.0.0.0', port=5000, debug=True)

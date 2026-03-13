from app import db
from datetime import datetime
import json
# 用户模型
class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(16), unique=True)
    email = db.Column(db.String(64), unique=True)
    avatar = db.Column(db.String(255))
    status = db.Column(db.SmallInteger, default=1, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'phone': self.phone,
            'email': self.email,
            'avatar': self.avatar,
            'created_at': self.created_at.isoformat()
        }
# 用户空间模型
class UserSpace(db.Model):
    __tablename__ = 'user_space'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    style = db.Column(db.String(32), nullable=False)
    size = db.Column(db.Integer, default=100, nullable=False)
    floor_count = db.Column(db.SmallInteger, default=1, nullable=False)
    has_yard = db.Column(db.SmallInteger, default=0, nullable=False)
    room_count = db.Column(db.SmallInteger, default=3, nullable=False)
    layout_config = db.Column(db.JSON, nullable=False)
    furniture_config = db.Column(db.JSON, nullable=False)
    preview_image = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'style': self.style,
            'size': self.size,
            'floor_count': self.floor_count,
            'has_yard': self.has_yard,
            'room_count': self.room_count,
            'layout_config': self.layout_config,
            'furniture_config': self.furniture_config,
            'preview_image': self.preview_image,
            'created_at': self.created_at.isoformat()
        }
# AI伴侣模型
class AICompanion(db.Model):
    __tablename__ = 'ai_companion'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    name = db.Column(db.String(32), nullable=False)
    avatar = db.Column(db.String(255), nullable=False)
    personality = db.Column(db.String(32), default='warm', nullable=False)
    feedback_count = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'avatar': self.avatar,
            'personality': self.personality,
            'feedback_count': self.feedback_count
        }
# 数字资产模型
class DigitalAsset(db.Model):
    __tablename__ = 'digital_asset'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    asset_id = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    category = db.Column(db.String(32), nullable=False)
    description = db.Column(db.Text)
    model_url = db.Column(db.String(255), nullable=False)
    cover_url = db.Column(db.String(255), nullable=False)
    carbon_reduction = db.Column(db.Numeric(8, 2), default=0.00, nullable=False)
    material = db.Column(db.String(32))
    recycle_status = db.Column(db.SmallInteger, default=0, nullable=False)
    position_config = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'asset_id': self.asset_id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'model_url': self.model_url,
            'cover_url': self.cover_url,
            'carbon_reduction': float(self.carbon_reduction),
            'material': self.material,
            'recycle_status': self.recycle_status,
            'position_config': self.position_config,
            'created_at': self.created_at.isoformat()
        }
# 成就模型
class Achievement(db.Model):
    __tablename__ = 'achievement'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    total_assets = db.Column(db.Integer, default=0, nullable=False)
    total_carbon_reduction = db.Column(db.Numeric(10, 2), default=0.00, nullable=False)
    medals = db.Column(db.JSON)
    rank = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total_assets': self.total_assets,
            'total_carbon_reduction': float(self.total_carbon_reduction),
            'medals': self.medals or [],
            'rank': self.rank,
            'updated_at': self.updated_at.isoformat()
        }
# 系统配置模型
class SystemConfig(db.Model):
    __tablename__ = 'system_config'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    config_key = db.Column(db.String(64), unique=True, nullable=False)
    config_value = db.Column(db.JSON, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    @classmethod
    def get_config(cls, key):
        config = cls.query.filter_by(config_key=key).first()
        return config.config_value if config else None
    
    def to_dict(self):
        return {
            'config_key': self.config_key,
            'config_value': self.config_value,
            'description': self.description
        }

from app import app, db
import os
# 创建数据库表（如果不存在）
with app.app_context():
    db.create_all()
    print("数据库表初始化完成")
if __name__ == '__main__':
    app.run(host=os.getenv('HOST', '0.0.0.0'), port=int(os.getenv('PORT', 5000)), debug=os.getenv('DEBUG', 'True') == 'True')

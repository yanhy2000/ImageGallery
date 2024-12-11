from app import app, db
import os
db_path = os.path.join("instance")  # 数据库文件存放路径
if not os.path.exists(db_path):
    os.makedirs(db_path)  # 如果目录不存在，创建目录
with app.app_context():
    db.create_all()
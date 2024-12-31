from app import app, db,utils
from app.controllers import user
import os
db_path = os.path.join(".")
if not os.path.exists(db_path):
    os.makedirs(db_path)
with app.app_context():
    db.create_all()

    # 创建初始管理员
    adminName = "admin"
    uuid = utils.generate_user_uuid()
    print(f"管理员用户初始化完毕！请保存初始登录信息：用户名{adminName}, token: {uuid}")
    new_user = user.User(username=adminName, usertoken=uuid, permissions=1)
    db.session.add(new_user)
    db.session.commit()
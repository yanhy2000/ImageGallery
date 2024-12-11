from flask import jsonify, request
from app import db
from app.models import User
from app.utils import generate_user_uuid

def add_new_user(usertoken):
    print(usertoken)
    data = request.get_json()

    # 获取用户名
    username = data.get('name')
    if not username:
        return jsonify({"code": 400, "message": "Username is required"}), 400
    # 根据usertoken查找用户
    user = User.query.filter_by(usertoken=usertoken).first()
    if not user:
        return jsonify({"code": 401, "message": "Token is invalid"}), 401
    # 判断用户名是否已存在
    if user.username == username:
        return jsonify({"code": 400, "message": "Username already exists"}), 400
    # 判断用户权限，如果小于1，返回权限不足，仅管理员可以创建新用户
    if user.permissions < 1:
        return jsonify({"code": 403, "message": "Permissions denied"}), 403

    # 创建新用户并保存到数据库
    new_user = User(username=username, usertoken=generate_user_uuid(), permissions=0)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "code": 200,
        "message": "success",
        "data": {
            "userid": new_user.userid,
            "username": new_user.username,
            "usertoken": new_user.usertoken
        }
    })

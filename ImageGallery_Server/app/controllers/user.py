from flask import jsonify, request
from app import db
from app.models import User
from app.utils import generate_user_uuid
from math import ceil
import re

def get_all_users(usertoken):
    user = User.query.filter_by(usertoken=usertoken).first()
    if not user:
        return jsonify({"code": 401, "message": "Token is invalid"}), 401
    if user.permissions < 1:
        return jsonify({"code": 403, "message": "Permissions denied"}), 403
    
    current_page = request.args.get('page', 1, type=int)
    per_page = request.args.get('perpage', 10, type=int)
    print(current_page, per_page)
    query = User.query
    pagination = query.paginate(page=current_page, per_page=per_page, error_out=False)
    users = pagination.items
    user_list = []
    total_users = pagination.total
    total_pages = ceil(total_users / per_page)
    user_list = []
    for u in users:
        user_list.append({
            "userid": u.userid,
            "username": u.username,
            "permissions": u.permissions,
            "usertoken": u.usertoken
        })
    return jsonify({
        "code": 200,
        "message": "success",
        "data": {
            "users": user_list,
            "per_page": per_page,
            "current_page": current_page,
            "totalUsers": total_users,
            "totalPages": total_pages
        }
    })

def register():
    data = request.get_json()
    username = data.get('username')
    usertoken = data.get('usertoken')
    if not username or not usertoken:
        return jsonify({"code": 401, "message": "Username and password are required"}), 403
    user = User.query.filter_by(username=username).first()
    if not user:
        if not re.match(r'^[a-zA-Z0-9]{6,20}$', usertoken):
            return jsonify({"code": 402, "message": "Password not allow"}), 403
        if not re.match(r'^[_0-9a-zA-Z][a-zA-Z0-9_]{3,16}$', username):
            return jsonify({"code": 403, "message": "Username not allow"}), 403

        new_user = User(username=username, usertoken=usertoken, permissions=0)
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
    else:
        return jsonify({"code": 400, "message": "Username already exists"}), 403


def add_new_user(usertoken):
    data = request.get_json()
    username = data.get('name')
    if not username:
        return jsonify({"code": 400, "message": "Username is required"}), 400
    user = User.query.filter_by(usertoken=usertoken).first()
    if not user:
        return jsonify({"code": 401, "message": "Token is invalid"}), 401
    if user.username == username:
        return jsonify({"code": 400, "message": "Username already exists"}), 400
    if user.permissions < 1:
        return jsonify({"code": 403, "message": "Permissions denied"}), 403
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

def get_username(user_id, usertoken):
    user = User.query.filter_by(userid=user_id, usertoken=usertoken).first()
    if not user:
        return jsonify({"code": 401, "message": "Token is invalid or user does not exist"}), 401
    if user.permissions < 1:
        return jsonify({"code": 403, "message": "Permissions denied"}), 403
    return jsonify({
        "code": 200,
        "message": "success",
        "data": {
            "username": user.username
        }
    })

# 删除用户
def delete_user(usertoken):
    data = request.get_json()
    user_id = data.get('userid')
    if not user_id:
        return jsonify({"code": 400, "message": "Userid is required"}), 400
    user = User.query.filter_by(usertoken=usertoken).first()#操作人
    deluser = User.query.filter_by(userid=user_id).first()
    if not user or not deluser:
        return jsonify({"code": 401, "message": "Token is invalid or user does not exist"}), 400
    if not deluser.userid == user_id or user.permissions < 1:
        return jsonify({"code": 401, "message": "Permissions denied"}), 401
    if deluser.username == data.get('name'):
        try:
            db.session.delete(deluser)
            db.session.commit()
            return jsonify({"code": 200, "message": "success"})
        except:
            return jsonify({"code": 500, "message": "Delete User Failed, Error occurred"}), 500
    elif deluser.username == data.get('name') and deluser.permissions == -2:
        return jsonify({"code": 400, "message": "User has been deleted"}), 400
    else:
        return jsonify({"code": 400, "message": "Username is not correct"}), 400

# 修改用户
def modify_user(usertoken):
    data = request.get_json()
    user_id = data.get('userid')
    username = data.get('name') 
    set_permissions = data.get('set_permissions')
    set_name = data.get('set_name') 
    regen_token = data.get('regen_token', False)
    if not user_id or not username:
        return jsonify({"code": 400, "message": "Userid and username are required"}), 400
    
    user = User.query.filter_by(usertoken=usertoken).first()  # 操作人
    moduser = User.query.filter_by(userid=user_id).first()  # 被修改的用户
    if not user or not moduser:
        return jsonify({"code": 401, "message": "Token is invalid or user does not exist"}), 400
    
    if moduser.userid == user.userid or user.permissions < 1:
        return jsonify({"code": 401, "message": "Permissions denied"}), 401

    if len(User.query.filter_by(username=username).all()) > 1:
        return jsonify({"code": 400, "message": "Username already exists"}), 400

    moduser.username = username
    if set_permissions is not None:
        moduser.permissions = set_permissions
    if set_name is not None:
        moduser.username = set_name

    # 重新生成Token
    if regen_token:
        moduser.usertoken = generate_user_uuid()
    db.session.commit()

    return jsonify({"code": 200, "message": "success", "data": {
        "userid": moduser.userid,
        "username": moduser.username,
        "permissions": moduser.permissions,
        "usertoken": moduser.usertoken
    }})
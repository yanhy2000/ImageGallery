from app import app
from flask import request, jsonify
from app.controllers import photo, album, user

# # 获取照片名列表
# @app.route('/api/photos', methods=['GET'])
# def get_photos():
#     return photo.get_all_photos()

# # 获取所有相册列表
# @app.route('/api/albums', methods=['GET'])
# def get_albums():
#     return album.get_all_albums()

# # 获取指定相册中的所有照片
# @app.route('/api/getphotosbyalbum', methods=['GET'])
# def get_photos_by_album():
#     album_id = request.args.get('album_id')
#     album_name = request.args.get('album_name')
#     if album_id:
#         return photo.get_photos_by_album_id(album_id)
#     elif album_name:
#         return photo.get_photos_by_album_name(album_name)
#     return jsonify({"code": 400, "message": "Invalid parameters"}), 400

# [ok]获取图片文件（根据photoid获取）
@app.route('/api/getphoto', methods=['GET'])
def get_photo():
    photo_id = request.args.get('photoid')
    if photo_id:
        thumbnail = request.args.get('thumbnail', 'true').lower() == 'true'
        return photo.get_photo_file(photo_id, thumbnail)
    return jsonify({"code": 400, "message": "photoid is required"}), 400

# [ok]获取图片信息
@app.route('/api/getphotoinfo', methods=['GET'])
def get_photo_info():
    usertoken = request.headers.get('Authorization')
    photo_id = request.args.get('photoid')
    if usertoken and photo_id:
        usertoken = usertoken.split("Bearer ")[1]
        return photo.get_photo_info(photo_id, usertoken)
    return jsonify({"code": 400, "message": "usertoken and photoid are required"}), 400

# [ok]获取用户名
@app.route('/api/getusername', methods=['GET'])
def get_username():
    usertoken = request.headers.get('Authorization')
    user_id = request.args.get('userid')
    if usertoken and user_id:
        usertoken = usertoken.split("Bearer ")[1]
        return user.get_username(user_id, usertoken)
    return jsonify({"code": 400, "message": "usertoken and userid are required"}), 400

# [ok]更新图片信息
@app.route('/api/updatephoto', methods=['POST'])
def update_photo():
    usertoken = request.headers.get('Authorization')
    if usertoken:
        data = request.get_json()
        usertoken = usertoken.split("Bearer ")[1]
        return photo.update_photo_info(data, usertoken)
    return jsonify({"code": 400, "message": "usertoken is required"}), 400

# [ok]上传照片
@app.route('/api/upload', methods=['POST'])
def upload_photo():
    usertoken = request.headers.get('Authorization')
    if usertoken:
        usertoken = usertoken.split("Bearer ")[1]
        return photo.upload_new_photo(usertoken)
    return jsonify({"code": 400, "message": "usertoken is required"}), 400

# 创建相册
@app.route('/api/createalbum', methods=['POST'])
def create_album():
    usertoken = request.headers.get('Authorization')
    if usertoken:
        data = request.get_json()
        return album.create_album(data, usertoken)
    return jsonify({"code": 400, "message": "usertoken is required"}), 400

# 删除相册
@app.route('/api/deletealbum', methods=['POST'])
def delete_album():
    usertoken = request.headers.get('Authorization')
    if usertoken:
        data = request.get_json()
        return album.delete_album(data, usertoken)
    return jsonify({"code": 400, "message": "usertoken is required"}), 400

# 获取相册信息
@app.route('/api/getalbuminfo', methods=['GET'])
def get_album_info():
    usertoken = request.headers.get('Authorization')
    album_id = request.args.get('albumid')
    if usertoken and album_id:
        usertoken = usertoken.split("Bearer ")[1]
        return album.get_album_info(album_id, usertoken)
    return jsonify({"code": 400, "message": "usertoken and albumid are required"}), 400

# 修改相册信息
@app.route('/api/setalbum', methods=['POST'])
def set_album():
    usertoken = request.headers.get('Authorization')
    if usertoken:
        data = request.get_json()
        return album.modify_album(data, usertoken)
    return jsonify({"code": 400, "message": "usertoken is required"}), 400


# 获取用户相册列表
@app.route('/api/getalbums', methods=['GET'])
def get_user_albums():
    usertoken = request.headers.get('Authorization')
    username = request.args.get('username')
    if usertoken:
        return album.get_user_albums(username, usertoken)
    return jsonify({"code": 400, "message": "usertoken is required"}), 400


# [ok]删除照片
@app.route('/api/deletephoto', methods=['POST'])
def delete_photo_route():
    # 获取请求中的参数
    data = request.get_json()
    usertoken = request.headers.get('Authorization').split("Bearer ")[1]
    photoid = data.get('photoid')
    if not usertoken or not photoid:
        return jsonify({"code": 400, "message": "usertoken and photoid are required"}), 400
    return photo.delete_photo(usertoken, photoid)

# [ok]新增用户
@app.route('/api/adduser', methods=['POST'])
def add_user():
    usertoken = request.headers.get('Authorization')
    if usertoken:
        usertoken = usertoken.split("Bearer ")[1]
        return user.add_new_user(usertoken)
    return jsonify({"code": 400, "message": "usertoken is required"}), 400

# [ok]删除用户
@app.route('/api/deluser', methods=['POST'])
def delete_user():
    usertoken = request.headers.get('Authorization')
    if usertoken:
        usertoken = usertoken.split("Bearer ")[1]
        return user.delete_user(usertoken)
    return jsonify({"code": 400, "message": "usertoken is required"}), 400

# [ok]修改用户
@app.route('/api/setuser', methods=['POST'])
def set_user():
    usertoken = request.headers.get('Authorization')
    if usertoken:
        usertoken = usertoken.split("Bearer ")[1]
        return user.modify_user(usertoken)
    return jsonify({"code": 400, "message": "usertoken is required"}), 400

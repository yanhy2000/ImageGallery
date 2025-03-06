from app import app
from flask import request, jsonify
from app.controllers import photo, album, user, like, comment
from app.models import Photo, Album, User
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.config import Config
from datetime import timedelta

app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
jwt = JWTManager(app)

@app.route('/api/checktoken', methods=['POST'])
def check_token():
    data = request.get_json()
    username = data.get('username')
    usertoken = data.get('usertoken')

    if not usertoken or not username:
        return jsonify({"code": 400, "message": "usertoken and username are required"}), 400

    user = User.query.filter_by(usertoken=usertoken).first()
    if user and user.username == username:
        if user.permissions >= 0:
            access_token = create_access_token(
                identity=username,
                additional_claims={"permissions": user.permissions},
                expires_delta=timedelta(hours=24)  # 设置 Token 过期时间
            )
            return jsonify({"code": 200, "message": "success", "data": {"allowlogin": True, "token": access_token}}), 200
        else:
            return jsonify({"code": 200, "message": "success", "data": {"allowlogin": False}}), 200
    else:
        return jsonify({"code": 401, "message": "usertoken is invalid"}), 401

@app.route('/api/protected', methods=['GET'])
@jwt_required()
def protected_route():
    current_user = get_jwt_identity()
    jwt_data = get_jwt() 

    user = User.query.filter_by(username=current_user).first()
    if user and user.permissions < 0: 
        return jsonify({"code": 403, "message": "用户已被封禁"}), 403
    return jsonify({
        "code": 200,
        "message": "success",
        "data": {
            "username": current_user,
            "permissions": jwt_data.get("permissions")
        }
    }), 200

# 拆分token
def split_token(request):
    try:
        return request.headers.get('Authorization').split("Bearer ")[1]
    except:
        return None

# 解析Json数据
# def parse_json(request):
#     try:
#         return request.get_json()
#     except:
#         return None

@app.route('/', methods=['GET'])
def index():
    return jsonify({"code": 200, "message": "Welcome to ImageGallery API"})

# [ok]获取公开照片列表
@app.route('/api/photos_list', methods=['GET'])
def get_photos():
    return photo.get_photo_list()

# [ok]获取图片详细信息列表
@app.route('/api/photolist', methods=['POST'])
def get_photolist():
    usertoken = split_token(request)
    if usertoken:
        return photo.get_photolist(usertoken)
    return jsonify({"code": 400, "message": "usertoken is required"}), 400

# [ok]获取所有相册列表
@app.route('/api/albumlist', methods=['POST'])
def get_albums():
    usertoken = split_token(request)
    if usertoken:
        return album.get_all_albums(usertoken)
    return jsonify({"code": 400, "message": "usertoken is required"}), 400
    
# [ok]获取所有用户列表
@app.route('/api/userlist', methods=['POST'])
def get_users():
    usertoken = split_token(request)
    if usertoken:
        return user.get_all_users(usertoken)
    return jsonify({"code": 400, "message": "usertoken is required"}), 400

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
        thumbnail = request.args.get('thumbnail', 'true')
        return photo.get_photo_file(photo_id, thumbnail)
    return jsonify({"code": 400, "message": "photoid is required"}), 400

# [ok]获取图片信息
@app.route('/api/getphotoinfo_all', methods=['GET'])
def get_photo_info_all():
    usertoken = split_token(request)
    photo_id = request.args.get('photoid')
    if usertoken and photo_id:
        return photo.get_photo_info_all(photo_id, usertoken)
    return jsonify({"code": 400, "message": "usertoken and photoid are required"}), 400

# [ok]获取图片展示信息
@app.route('/api/getphotoinfo', methods=['GET'])
def get_photo_info():
    photo_id = request.args.get('photoid')
    if photo_id:
        return photo.get_photo_info(photo_id)
    return jsonify({"code": 400, "message": "usertoken and photoid are required"}), 400

# [ok]获取用户名
@app.route('/api/getusername', methods=['GET'])
def get_username():
    usertoken = split_token(request)
    user_id = request.args.get('userid')
    if usertoken and user_id:
        return user.get_username(user_id, usertoken)
    return jsonify({"code": 400, "message": "usertoken and userid are required"}), 400

# [ok]更新图片信息
@app.route('/api/updatephoto', methods=['POST'])
def update_photo():
    usertoken = split_token(request)
    if usertoken:
        return photo.update_photo_info(usertoken)
    return jsonify({"code": 400, "message": "usertoken is required"}), 400

# [ok]上传照片
@app.route('/api/upload', methods=['POST'])
def upload_photo():
    usertoken = split_token(request)
    if usertoken:
        return photo.upload_new_photo(usertoken)
    return jsonify({"code": 400, "message": "usertoken is required"}), 400

# [ok]删除照片
@app.route('/api/deletephoto', methods=['POST'])
def delete_photo_route():
    usertoken = split_token(request)
    if usertoken:
        return photo.delete_photo(usertoken)
    return jsonify({"code": 400, "message": "usertoken and photoid are required"}), 400
    
# [ok]新增用户
@app.route('/api/adduser', methods=['POST'])
def add_user():
    usertoken = split_token(request)
    if usertoken:
        return user.add_new_user(usertoken)
    return jsonify({"code": 400, "message": "usertoken is required"}), 400

# [ok]删除用户
@app.route('/api/deluser', methods=['POST'])
def delete_user():
    usertoken = split_token(request)
    if usertoken:
        return user.delete_user(usertoken)
    return jsonify({"code": 400, "message": "usertoken is required"}), 400

# [ok]修改用户
@app.route('/api/setuser', methods=['POST'])
def set_user():
    usertoken = split_token(request)
    if usertoken:
        return user.modify_user(usertoken)
    return jsonify({"code": 400, "message": "usertoken is required"}), 400

# [ok]创建相册
@app.route('/api/createalbum', methods=['POST'])
def create_album():
    usertoken = split_token(request)
    if usertoken:
        return album.create_album(usertoken)
    return jsonify({"code": 400, "message": "usertoken is required"}), 400

# [ok]删除相册
@app.route('/api/deletealbum', methods=['POST'])
def delete_album():
    usertoken = split_token(request)
    if usertoken:
        return album.delete_album(usertoken)
    return jsonify({"code": 400, "message": "usertoken is required"}), 400

# [ok]修改相册信息
@app.route('/api/setalbum', methods=['POST'])
def set_album():
    usertoken = split_token(request)
    if usertoken:
        return album.modify_album(usertoken)
    return jsonify({"code": 400, "message": "usertoken is required"}), 400

# 点赞图片
@app.route('/api/likephoto', methods=['POST'])
def like_photo():
    usertoken = split_token(request)
    if usertoken:
        return like.like_photo(usertoken)
    return jsonify({"code": 400, "message": "usertoken is required"}), 400

# 取消点赞图片
@app.route('/api/unlikephoto', methods=['POST'])
def unlike_photo():
    usertoken = split_token(request)
    if usertoken:
        return like.unlike_photo(usertoken)
    return jsonify({"code": 400, "message": "usertoken is required"}), 400

# 获取图片总点赞数
@app.route('/api/getphotolikecount', methods=['GET'])
def get_photo_like_count():
    photo_id = request.args.get('photoid')
    if photo_id:
        return like.get_photo_like_count(photo_id)
    return jsonify({"code": 400, "message": "photoid is required"}), 400

# 发表评论
@app.route('/api/commentphoto', methods=['POST'])
def comment_photo():
    usertoken = split_token(request)
    if usertoken:
        return comment.comment_photo(usertoken)
    return jsonify({"code": 400, "message": "usertoken is required"}), 400

# 删除评论
@app.route('/api/deletecomment', methods=['POST'])
def delete_comment():
    usertoken = split_token(request)
    if usertoken:
        return comment.delete_comment(usertoken)
    return jsonify({"code": 400, "message": "usertoken is required"}), 400

# 获取评论列表
@app.route('/api/getcomments', methods=['GET'])
def get_comments():
    usertoken = split_token(request)
    photo_id = request.args.get('photoid')
    if usertoken and photo_id:
        return comment.get_comments(photo_id, usertoken)
    return jsonify({"code": 400, "message": "usertoken and photoid are required"}), 400

# 点赞评论
@app.route('/api/likecomment', methods=['POST'])
def like_comment():
    usertoken = split_token(request)
    if usertoken:
        return like.like_comment(usertoken)
    return jsonify({"code": 400, "message": "usertoken is required"}), 400

# 取消点赞评论
@app.route('/api/unlikecomment', methods=['POST'])
def unlike_comment():
    usertoken = split_token(request)
    if usertoken:
        return like.unlike_comment(usertoken)
    return jsonify({"code": 400, "message": "usertoken is required"}), 400


# 获取评论总点赞数
@app.route('/api/getcommentlikecount', methods=['GET'])
def get_comment_like_count():
    comment_id = request.args.get('commentid')
    if comment_id:
        return like.get_comment_like_count(comment_id)
    return jsonify({"code": 400, "message": "commentid is required"}), 400
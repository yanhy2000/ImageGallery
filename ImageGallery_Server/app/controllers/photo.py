import os
from PIL import Image
from app import db
from app.models import Photo, Album, User, Like, Comment
from app.controllers import photo, album, user, like, comment
from flask import request, jsonify, send_file
from app.utils import generate_uuid_filename, get_project_root, get_utc_time,utc_to_local
from datetime import datetime
from app.config import Config
from math import ceil
from sqlalchemy import desc
from flask_jwt_extended import jwt_required, get_jwt_identity

# 获取照片列表（公开）
def get_photo_list():
    current_page = request.args.get('page', 1, type=int)
    per_page = request.args.get('perpage', 10, type=int)
    query = Photo.query.order_by(desc(Photo.upload_time))
    pagination = query.paginate(page=current_page, per_page=per_page, error_out=False)
    photos = pagination.items
    photo_list = []
    total_photos = pagination.total
    total_pages = ceil(total_photos / per_page)
    for photo in photos:
        username = User.query.filter_by(userid=photo.userid).first().username
        photo_list.append({
            "photoid": photo.photoid,
            "desc": photo.desc if photo.desc else "无描述",
            "upload_time": photo.upload_time.strftime("%Y-%m-%d %H:%M:%S"),
            "upload_user": username, 
            "thumbnail": photo.thumbnail,
            "likes": like.get_comment_like_count(photo.photoid),
        })
    return jsonify({
        "code": 200,
        "message": "success",
        "data": {
            "tatolPhotos": total_photos,
            "totalPages": total_pages,
            "per_page": per_page,
            "current_page": current_page,
            "photos": photo_list 
        }
    })

# 获取图片列表(后台管理)
def get_photolist(usertoken):
    user = User.query.filter_by(usertoken=usertoken).first()
    if not user:
        return jsonify({"code": 401, "message": "token failed"}), 401
    if user.permissions < 1:
        return jsonify({"code": 403, "message": "permission denied"}), 403
    current_page = request.args.get('page', 1, type=int)
    per_page = request.args.get('perpage', 10, type=int)
    query = Photo.query
    pagination = query.paginate(page=current_page, per_page=per_page, error_out=False)
    photos = pagination.items
    photo_list = []
    total_photos = pagination.total
    total_pages = ceil(total_photos / per_page)
    for photo in photos:
        album = Album.query.filter_by(albumid=photo.albumid).first()
        photo_list.append({
            "photoid": photo.photoid,
            "name": photo.name,
            "desc": photo.desc,
            "upload_time": photo.upload_time.strftime("%Y-%m-%d %H:%M:%S"),
            "thumbnail": photo.thumbnail,
            "photo_url": photo.photo_url,
            "album_name": album.name,
            "albumid": photo.albumid,
            "userid": photo.userid,
            "username": User.query.filter_by(userid=photo.userid).first().username
        })
    return jsonify({
        "code": 200,
        "message": "success",
        "data": {
            "tatolPhotos": total_photos,
            "totalPages": total_pages,
            "per_page": per_page,
            "current_page": current_page,
            "photos": photo_list
        }
    })

# 获取用户自己的照片列表
def get_user_photos():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    if not user:
        return jsonify({"code": 401, "message": "token failed"}), 401
    if user.permissions < 0:
        return jsonify({"code": 403, "message": "permission denied"}), 403

    current_page = request.args.get('page', 1, type=int)
    per_page = request.args.get('perpage', 10, type=int)
    
    photos_query = db.session.query(
        Photo,
        Album.name.label('album_name'),
        db.func.count(Like.photoid).label('like_count'),
        db.func.group_concat(User.username).label('liked_usernames')
    ).join(
        Album, Album.albumid == Photo.albumid
    ).outerjoin(
        Like, Like.photoid == Photo.photoid
    ).outerjoin(
        User, User.userid == Like.userid
    ).filter(
        Photo.userid == user.userid
    ).group_by(
        Photo.photoid
    )

    pagination = photos_query.paginate(page=current_page, per_page=per_page, error_out=False)
    items = pagination.items
    total_photos = pagination.total
    total_pages = ceil(total_photos / per_page)

    photo_list = []
    for photo, album_name, like_count, liked_usernames in items:
        photo_list.append({
            "photoid": photo.photoid,
            "thumbnail": photo.thumbnail,
            "desc": photo.desc,
            "like_count": like_count or 0,
            "liked_users": liked_usernames.split(',') if liked_usernames else [],
            "album_name": album_name,
            "upload_time": photo.upload_time.strftime("%Y-%m-%d %H:%M:%S"),
        })

    return jsonify({
        "code": 200,
        "message": "success",
        "data": {
            "tatolPhotos": total_photos,
            "totalPages": total_pages,
            "per_page": per_page,
            "current_page": current_page,
            "photos": photo_list
        }
    })

# 创建本地缩略图
def create_thumbnail(image_path):
    with Image.open(image_path) as img:
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        img.thumbnail((900, 900))  # 设置缩略图最大尺寸
        thumbnail_path_dir = os.path.join("uploads/.thumbnails")
        if not os.path.exists(thumbnail_path_dir):
            os.makedirs(thumbnail_path_dir)
        thumbnail_path = f"{thumbnail_path_dir}/{generate_uuid_filename()}.jpg"
        img.save(thumbnail_path, format="JPEG")

        if not Config.SAVE_ORIGINAL_IMAGE:
            os.remove(image_path)
        return thumbnail_path

# 删除缩略图
def del_thumbnail(photo_id):
    photo = Photo.query.filter_by(photoid=photo_id).first()
    if not photo:
        return jsonify({"code": 404, "message": "Photo not found"}), 404
    thumbnail_url = photo.thumbnail
    if thumbnail_url.startswith("uploads/.thumbnails/"):
        os.remove(thumbnail_url)
        return jsonify({"code": 200, "message": "Thumbnail deleted"}), 200
    return jsonify({"code": 200, "message": "success"}), 200

        
# 上传新照片
def upload_new_photo(usertoken):
    user = User.query.filter_by(usertoken=usertoken).first()
    if not user:
        return jsonify({"code": 401, "message": "token failed"}), 401
    if user.permissions < 0:
        return jsonify({"code": 403, "message": "permission denied"}), 403
    file = request.files.get("file")
    name =request.form.get("name", file.filename)
    desc = request.form.get("desc", "无描述")
    album_name = request.form.get("album", user.username)
    if album_name == "":
        album_name = user.username

    if not file:
        return jsonify({"code": 404, "message": "need file"}), 404

    today = get_utc_time()
    year = today.year
    month = today.month
    day = today.day

    upload_dir = os.path.join('uploads', str(year).zfill(2), str(month).zfill(2), str(day).zfill(2))
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # 处理文件名
    filename = generate_uuid_filename() + os.path.splitext(file.filename)[-1]
    file_path = os.path.join(upload_dir, filename)
    file.save(file_path)
    try:
        thumbnail_url = create_thumbnail(file_path)
        album = Album.query.filter_by(name=album_name, userid=user.userid).first()
        if not album:
            album = Album(name=album_name, userid=user.userid)
            db.session.add(album)
            db.session.commit()

        new_photo = Photo(
            name=name or file.filename,
            desc=desc,
            upload_time=get_utc_time(),
            thumbnail=thumbnail_url,
            photo_url=file_path,
            albumid=album.albumid,
            userid=user.userid
        )

        db.session.add(new_photo)
        db.session.commit()
    except Exception as e:
        print("upload_new_photo error:",e)
        return jsonify({"code": 500, "message": f"error:{e}"}), 500
    # 返回成功响应
    return jsonify({
        "code": 200,
        "message": "success",
        "data": new_photo.photoid
    })

# 上传照片-新接口
def upload_photo():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({"code": 401, "message": "token failed"}), 401
    if user.permissions < 0:
        return jsonify({"code": 403, "message": "permission denied"}), 403
    file = request.files.get("file")
    name =request.form.get("name", file.filename)
    desc = request.form.get("desc", "无描述")
    album_name = request.form.get("album", user.username)
    if album_name == "":
        album_name = user.username

    if not file:
        return jsonify({"code": 404, "message": "need file"}), 404

    today = get_utc_time()
    year = today.year
    month = today.month
    day = today.day

    upload_dir = os.path.join('uploads', str(year).zfill(2), str(month).zfill(2), str(day).zfill(2))
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # 处理文件名
    filename = generate_uuid_filename() + os.path.splitext(file.filename)[-1]
    file_path = os.path.join(upload_dir, filename)
    file.save(file_path)
    try:
        thumbnail_url = create_thumbnail(file_path)
        album = Album.query.filter_by(name=album_name, userid=user.userid).first()
        if not album:
            album = Album(name=album_name, userid=user.userid)
            db.session.add(album)
            db.session.commit()

        new_photo = Photo(
            name=name or file.filename,
            desc=desc,
            upload_time=get_utc_time(),
            thumbnail=thumbnail_url,
            photo_url=file_path,
            albumid=album.albumid,
            userid=user.userid
        )

        db.session.add(new_photo)
        db.session.commit()
    except Exception as e:
        print("upload_photo error:",e)
        return jsonify({"code": 500, "message": f"error:{e}"}), 500
    # 返回成功响应
    return jsonify({
        "code": 200,
        "message": "success",
        "data": new_photo.photoid
    })

# 删除照片
def delete_photo(usertoken):
    data = request.get_json()
    photoid = data.get('photoid')
    user = User.query.filter_by(usertoken=usertoken).first()
    if not user:
        return jsonify({"code": 401, "message": "token failed"}), 401
    photo = Photo.query.filter_by(photoid=photoid).first()
    if not photo:
        return jsonify({"code": 404, "message": "Photo not found"}), 404
    # 检查用户是否有权限删除该照片（如果是上传者或者管理员可以删除）
    if user.permissions < 1:
        return jsonify({"code": 403, "message": "permission denied"}), 403

    # 删除本地存储的图片文件
    try:
        # 删除缩略图文件
        thu = del_thumbnail(photoid)
        if thu[1] == 200:
            pass
        else:
            return jsonify({"code": 201, "message": f"Error deleting thumbnail:{thu}"}), 500
        # 删除原图文件
        file_path = photo.photo_url
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        return jsonify({"code": 500, "message": f"Error deleting files: {str(e)}"}), 500

    # 删除数据库中的照片记录
    try:
        Like.query.filter_by(photoid=photoid).delete()
        Comment.query.filter_by(photoid=photoid).delete()

        db.session.delete(photo)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "message": f"Error deleting from database: {str(e)}"}), 500

    return jsonify({"code": 200, "message": "Photo deleted successfully"}), 200

# 新-删除用户自己的照片
def del_user_photo():
    data = request.get_json()
    photoid = data.get('photoid')
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({"code": 401, "message": "token failed"}), 401

    photo = Photo.query.filter_by(photoid=photoid).first()
    if not photo:
        return jsonify({"code": 404, "message": "Photo not found"}), 404

    # 检查用户是否有权限删除该照片（上传者以上可以删除）
    if photo.userid != user.userid or user.permissions < 0:
        return jsonify({"code": 403, "message": "permission denied"}), 403

    # 删除本地存储的图片文件
    try:
        # 删除缩略图文件
        thu = del_thumbnail(photoid)
        if thu[1] == 200:
            pass
        else:
            return jsonify({"code": 201, "message": f"Error deleting thumbnail:{thu}"}), 500
        # 删除原图文件
        file_path = photo.photo_url
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        return jsonify({"code": 500, "message": f"Error deleting files: {str(e)}"}), 500

    # 删除数据库中的照片记录
    try:
        Like.query.filter_by(photoid=photoid).delete()
        Comment.query.filter_by(photoid=photoid).delete()
        db.session.delete(photo)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "message": f"Error deleting from database: {str(e)}"}), 500

    return jsonify({"code": 200, "message": "Photo deleted successfully"}), 200



# 下载照片（通过photo_id获取文件；如果thumbnail为1，则获取缩略图）
def get_photo_file(photo_id, thumbnail=1):
    photo = Photo.query.filter_by(photoid=photo_id).first()
    isattachment = False
    if not photo:
        return jsonify({"code": 404, "message": "Photo not found"}), 404

    # # 获取文件路径
    # if thumbnail==1:
        
    # else:
    #     if Config.SAVE_ORIGINAL_IMAGE: 
    #         file_path = os.path.join(get_project_root(), photo.photo_url)
    #     else: # 如果不保存原图，则返回缩略图，供后台使用
    #         file_path = os.path.join(get_project_root(), photo.thumbnail)
    #     isattachment = True
    file_path = os.path.join(get_project_root(), photo.thumbnail)
    if not os.path.exists(file_path):
        return jsonify({"code": 404, "message": "File not found"}), 404

    try:
        return send_file(file_path, as_attachment=isattachment)
    except Exception as e:
        return jsonify({"code": 500, "message": f"Error reading file: {str(e)}"}), 500

# 获取照片信息
def get_photo_info_all(photo_id, usertoken):
    user = User.query.filter_by(usertoken=usertoken).first()
    if not user:
        return jsonify({"code": 401, "message": "token failed"}), 401
    photo = Photo.query.filter_by(photoid=photo_id).first()
    if not photo:
        return jsonify({"code": 404, "message": "Photo not found"}), 404
    if photo.userid != user.userid and user.permissions < 0:
        return jsonify({"code": 403, "message": "permission denied"}), 403
    albumname = Album.query.filter_by(albumid=photo.albumid).first().name
    return jsonify({
        "code": 200,
        "message": "success",
        "data": {
            "photoid": photo.photoid,
            "name": photo.name,
            "desc": photo.desc,
            "upload_time": photo.upload_time.strftime("%Y-%m-%d %H:%M:%S"),
            "thumbnail": photo.thumbnail,
            "photo_url": photo.photo_url,
            "albumname": albumname,
            "userid": photo.userid
        }
    })

# 获取照片公开展示信息（包含desc、userid、uploader、thumbnail、upload_time）
def get_photo_info(photo_id):
    photo = Photo.query.filter_by(photoid=photo_id).first()
    username = User.query.filter_by(userid=photo.userid).first().username
    if not photo:
        return jsonify({"code": 404, "message": "Photo not found"}), 404
    albumname = Album.query.filter_by(albumid=photo.albumid).first().name
    return jsonify({
        "code": 200,
        "message": "success",
        "data": {
            "photoid": photo.photoid,
            "name": photo.name,
            "desc": photo.desc,
            "upload_time": photo.upload_time.strftime("%Y-%m-%d %H:%M:%S"),
            "uploader": username,
            "thumbnail": photo.thumbnail,
            "photo_url": photo.photo_url,
            "albumname": albumname,
            "userid": photo.userid
        }
    })

# 更新照片信息
def update_photo_info(usertoken):
    data = request.get_json()
    user = User.query.filter_by(usertoken=usertoken).first()
    photoid = data.get("photoid")
    if not user:
        return jsonify({"code": 401, "message": "token failed"}), 401
    photo = Photo.query.filter_by(photoid=photoid).first()
    if not photo:
        return jsonify({"code": 404, "message": "Photo not found"}), 404
    if photo.userid != user.userid and user.permissions < 0:
        return jsonify({"code": 403, "message": "permission denied"}), 403

    # 更新数据库记录
    try:
        if "name" in data:
            photo.name = data["name"]
        if "desc" in data:
            photo.desc = data["desc"]
        if "albumid" in data:
            album = Album.query.filter_by(albumid=data["albumid"]).first()
            if not album:
                return jsonify({"code": 400, "message": "album not found, please create album first"}), 400
            photo.albumid = data["albumid"]
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "message": f"Error updating database: {str(e)}"}), 500

    return jsonify({"code": 200, "message": "Photo updated successfully"}), 200






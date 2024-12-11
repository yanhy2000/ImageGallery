import os
from PIL import Image
from io import BytesIO
import requests
import re
from app import db
from app.models import Photo, Album, User
from flask import request, jsonify
from werkzeug.utils import secure_filename
from app.utils import generate_uuid_filename
from datetime import datetime
from app.config import Config


# 生成缩略图并上传到外部服务器
def create_thumbnail(image_path):
    # 使用PIL打开图片
    with Image.open(image_path) as img:
        img.thumbnail((900, 900))  # 设置缩略图最大尺寸
        thumbnail_path = f"uploads/.thumbnails/{generate_uuid_filename()}.jpg"  # 存放缩略图的路径

        # 保存缩略图到本地
        img.save(thumbnail_path, format="JPEG")

        # 上传缩略图到外部服务器
        url = "https://api.superbed.cn/upload"
        with open(thumbnail_path, "rb") as f:
            resp = requests.post(url, data={"token": config.SUPERBED_TOKEN}, files={"file": f})

        if resp.status_code == 200:
            # 删除本地缩略图
            os.remove(thumbnail_path)
            return resp.json().get("url")  # 返回上传后的外部URL
        return None

# 删除云端缩略图
def del_thumbnail(photo_id):
    # 获取照片记录
    photo = Photo.query.filter_by(photoid=photo_id).first()
    if not photo:
        return jsonify({"code": 404, "message": "Photo not found"}), 404

    # 提取缩略图的ID
    thumbnail_url = photo.thumbnail
    match = re.search(r'/item/([a-f0-9]+)', thumbnail_url)
    if not match:
        return jsonify({"code": 400, "message": "Invalid thumbnail URL"}), 400

    thumbnail_id = match.group(1)  # 提取出来的图片ID

    # 构建删除请求的URL
    api_url = f'https://api.superbed.cn/info/{thumbnail_id}'
    data = {
        'token': config.SUPERBED_TOKEN,
        'action': 'delete'
    }

    # 发送POST请求删除云端图片
    try:
        response = requests.post(api_url, data=data)
        result = response.json()

        if result.get('err') == 0:
            return jsonify({"code": 200, "message": "Thumbnail deleted successfully"}), 200
        else:
            return jsonify({"code": 500, "message": f"Error: {result.get('msg')}"}, 500)
    except requests.RequestException as e:
        return jsonify({"code": 500, "message": f"Request error: {str(e)}"}), 500
        
# 上传新照片
def upload_new_photo(usertoken):
    # 验证用户token
    user = User.query.filter_by(usertoken=usertoken).first()
    if not user:
        return jsonify({"code": 401, "message": "token failed"}), 401
    # 判断用户权限，如果小于0，返回权限不足
    if user.permissions < 0:
        return jsonify({"code": 403, "message": "permission denied"}), 403
    # 获取上传的文件和参数
    file = request.files.get("file")
    name = request.form.get("name", "无名")
    desc = request.form.get("desc", "无描述")
    album_name = request.form.get("album", user.username)

    # 生成UUID文件名并保存文件
    if not file:
        return jsonify({"code": 400, "message": "need file"}), 400

    # 获取当前日期
    today = datetime.utcnow()
    month = today.month  # 当前月份
    day = today.day      # 当前日期

    # 创建存储路径
    upload_dir = os.path.join('uploads', str(month).zfill(2), str(day).zfill(2))
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)  # 如果目录不存在，创建目录

    # 处理文件名
    filename = generate_uuid_filename() + os.path.splitext(file.filename)[-1]
    file_path = os.path.join(upload_dir, filename)  # 存储路径
    file.save(file_path)  # 保存文件到指定路径

    try:
        # 生成缩略图并上传
        thumbnail_url = create_thumbnail(file_path)

        # 保存图片信息到数据库
        album = Album.query.filter_by(name=album_name, userid=user.userid).first()
        if not album:
            # 如果相册不存在，创建新相册
            album = Album(name=album_name, userid=user.userid)
            db.session.add(album)
            db.session.commit()

        new_photo = Photo(
            name=name or file.filename,
            desc=desc,
            upload_time=datetime.utcnow(),
            thumbnail=thumbnail_url,
            photo_url=file_path,
            albumid=album.albumid,
            userid=user.userid
        )

        db.session.add(new_photo)
        db.session.commit()
    except Exception as e:
        return jsonify({"code": 500, "message": f"error:{e}"}), 500
    # 返回成功响应
    return jsonify({
        "code": 200,
        "message": "success",
        "data": {
            "photoid": new_photo.photoid
        }
    })

# 删除照片
def delete_photo(usertoken, photoid):
    # 根据usertoken查找用户
    user = User.query.filter_by(usertoken=usertoken).first()
    if not user:
        return jsonify({"code": 401, "message": "token failed"}), 401
    # 判断用户权限，如果小于0，返回权限不足
    if user.permissions < 0:
        return jsonify({"code": 403, "message": "permission denied"}), 403
    # 根据photoid查找照片记录
    photo = Photo.query.filter_by(photoid=photoid).first()
    if not photo:
        return jsonify({"code": 404, "message": "Photo not found"}), 404

    # 检查用户是否有权限删除该照片（如果是上传者或者管理员可以删除）
    if photo.userid != user.userid and user.permissions < 0:
        return jsonify({"code": 403, "message": "非管理员只能删除自己的图片"}), 403

    # 删除本地存储的图片文件
    try:
        # 拼接文件路径，删除文件
        file_path = photo.photo_url  # 假设 photo_url 存储了图片的存储路径
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # 删除缩略图文件
        del_thumbnail(photo.photoid)
    except Exception as e:
        return jsonify({"code": 500, "message": f"Error deleting files: {str(e)}"}), 500

    # 删除数据库中的照片记录
    try:
        db.session.delete(photo)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "message": f"Error deleting from database: {str(e)}"}), 500

    return jsonify({"code": 200, "message": "Photo deleted successfully"}), 200
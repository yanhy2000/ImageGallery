from flask import jsonify, request
from app.models import Album
from app.models import Photo, Album, User
from app import db
from app.utils import utc_to_local,get_utc_time
import os
from math import ceil
from flask_jwt_extended import jwt_required, get_jwt_identity

# 获取所有相册列表
def get_all_albums(usertoken):
    user = User.query.filter_by(usertoken=usertoken).first()
    if not user:
        return jsonify({"code": 401, "message": "token failed"}), 401
    if user.permissions < 1:
        return jsonify({"code": 403, "message": "permission denied"}), 403
    
    current_page = request.args.get('page', 1, type=int)
    per_page = request.args.get('perpage', 10, type=int)
    query = Album.query
    pagination = query.paginate(page=current_page, per_page=per_page, error_out=False)
    albums = pagination.items
    album_list = []
    total_albums = pagination.total
    total_pages = ceil(total_albums / per_page)
    for album in albums:
        album_list.append({
            'albumid': album.albumid,
            'name': album.name,
            'userid': album.userid,
            'create_time': album.create_time.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify({
            "code": 200,
            "message": "success",
            "data": {
                "tatolAlbums": total_albums,
                "totalPages": total_pages,
                "per_page": per_page,
                "current_page": current_page,
                "albums": album_list
            }
        })

# 获取用户自己的相册列表
def get_user_albums():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    if not user:
        return jsonify({"code": 401, "message": "token failed"}), 401
    if user.permissions < 0:
        return jsonify({"code": 403, "message": "permission denied"}), 403
    
    current_page = request.args.get('page', 1, type=int)
    per_page = request.args.get('perpage', 10, type=int)
    query = Album.query.filter_by(userid=user.userid)
    pagination = query.paginate(page=current_page, per_page=per_page, error_out=False)
    albums = pagination.items
    album_list = []
    total_albums = pagination.total
    total_pages = ceil(total_albums / per_page)
    for album in albums:
        album_list.append({
            'albumid': album.albumid,
            'name': album.name,
            'create_time': album.create_time.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify({
            "code": 200,
            "message": "success",
            "data": {
                "tatolAlbums": total_albums,
                "totalPages": total_pages,
                "per_page": per_page,
                "current_page": current_page,
                "albums": album_list
            }
        })


# 新建相册
def create_album(usertoken):
    user = User.query.filter_by(usertoken=usertoken).first()
    if not user:
        return jsonify({"code": 401, "message": "token failed"}), 401
    if user.permissions < 1:
        return jsonify({"code": 403, "message": "permission denied"}), 403
    
    name = request.json.get('name')
    if not name:
        return jsonify({"code": 400, "message": "name is required"}), 400
    
    album = Album(name=name, userid=user.userid,create_time=get_utc_time())
    db.session.add(album)
    db.session.commit()
    
    return jsonify({
            "code": 200,
            "message": "success",
            "data": {
                "albumid": album.albumid
            }
        })

# 删除相册
def delete_album(usertoken):
    user = User.query.filter_by(usertoken=usertoken).first()
    if not user:
        return jsonify({"code": 401, "message": "token failed"}), 401
    if user.permissions < 1:
        return jsonify({"code": 403, "message": "permission denied"}), 403
    
    albumid = request.json.get('albumid')
    if not albumid:
        return jsonify({"code": 400, "message": "albumid is required"}), 400
    album = Album.query.filter_by(albumid=albumid).first()
    if not album:
        return jsonify({"code": 404, "message": "album not found"}), 404
    
    # 删除相册下的所有照片
    photos = Photo.query.filter_by(albumid=albumid).all()
    for photo in photos:
        try:
            file_path = photo.photo_url
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(e)
        db.session.delete(photo)
        db.session.commit()

    # 删除相册
    db.session.delete(album)
    db.session.commit()
    
    return jsonify({
            "code": 200,
            "message": "success"
        })

# 新-删除用户自己的相册
def del_user_album():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    if not user:
        return jsonify({"code": 401, "message": "token failed"}), 401

    albumid = request.json.get('albumid')
    if not albumid:
        return jsonify({"code": 400, "message": "albumid is required"}), 400
    album = Album.query.filter_by(albumid=albumid).first()
    if not album:
        return jsonify({"code": 404, "message": "album not found"}), 404
    if album.userid != user.userid or user.permissions < 0:
        return jsonify({"code": 403, "message": "permission denied"}), 403
        
    # 删除相册下的所有照片
    photos = Photo.query.filter_by(albumid=albumid).all()
    for photo in photos:
        try:
            file_path = photo.photo_url
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(e)
        db.session.delete(photo)
        db.session.commit()

    # 删除相册
    db.session.delete(album)
    db.session.commit()
    
    return jsonify({
            "code": 200,
            "message": "success"
        })

# 编辑相册
def modify_album(usertoken):
    user = User.query.filter_by(usertoken=usertoken).first()
    if not user:
        return jsonify({"code": 401, "message": "token failed"}), 401
    if user.permissions < 1:
        return jsonify({"code": 403, "message": "permission denied"}), 403
    
    albumid = request.json.get('albumid')
    if not albumid:
        return jsonify({"code": 400, "message": "albumid is required"}), 400
    album = Album.query.filter_by(albumid=albumid).first()
    if not album:
        return jsonify({"code": 404, "message": "album not found"}), 404
    
    name = request.json.get('name')
    if name is not None:
        album.name = name
    else:
        return jsonify({"code": 400, "message": "no modification"}), 400
    
    db.session.commit()
    
    return jsonify({
            "code": 200,
            "message": "success"
        })
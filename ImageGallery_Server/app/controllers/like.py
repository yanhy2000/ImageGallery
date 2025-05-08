from app import db
from app.models import Photo, User, Like, Comment, CommentLike
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from math import ceil

# [ok]新-获取图片点赞的用户
# def get_likedUsers():
#     current_user = get_jwt_identity()
#     user = User.query.filter_by(username=current_user).first()

#     if not user:
#         return jsonify({"code": 401, "message": "token failed"}), 401
#     if user.permissions < 0:
#         return jsonify({"code": 403, "message": "permission denied"}), 403

#     current_page = request.args.get('page', 1, type=int)
#     per_page = request.args.get('perpage', 10, type=int)
#     query = Photo.query.filter_by(userid=user.userid)
#     pagination = query.paginate(page=current_page, per_page=per_page, error_out=False)
#     photos = pagination.items
#     photo_list = []
#     total_photos = pagination.total
#     total_pages = ceil(total_photos / per_page)
#     for photo in photos:
#         album = Album.query.filter_by(albumid=photo.albumid).first()
#         like_count = Like.query.filter_by(photoid=photo.photoid).count()
#         photo_list.append({
#             "photoid": photo.photoid,
#             "thumbnail": photo.thumbnail,
#             "desc": photo.desc,
#             "like_count": like_count,
#             "album_name": album.name,
#             "upload_time": photo.upload_time.strftime("%Y-%m-%d %H:%M:%S"),
#         })
#     return jsonify({
#         "code": 200,
#         "message": "success",
#         "data": {
#             "tatolPhotos": total_photos,
#             "totalPages": total_pages,
#             "per_page": per_page,
#             "current_page": current_page,
#             "photos": photo_list
#         }
#     })
# 照片点赞
def like_photo():
    data = request.get_json()
    photo_id = data.get("photoid")
    if not photo_id:
        return jsonify({"code": 400, "message": "photoid is required"}), 400

    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({"code": 401, "message": "User not found"}), 401

    if user.permissions < 0:
        return jsonify({"code": 403, "message": "Permissions denied"}), 403

    photo = Photo.query.filter_by(photoid=photo_id).first()
    if not photo:
        return jsonify({"code": 404, "message": "Photo not found"}), 404

    like = Like.query.filter_by(userid=user.userid, photoid=photo_id).first()
    if like:
        return jsonify({"code": 400, "message": "Already liked"}), 400

    new_like = Like(userid=user.userid, photoid=photo_id)
    db.session.add(new_like)
    db.session.commit()

    return jsonify({"code": 200, "message": "Liked successfully"}), 200
    
# 取消照片点赞
def unlike_photo():
    data = request.get_json()
    photo_id = data.get("photoid") 

    if not photo_id:
        return jsonify({"code": 400, "message": "photoid is required"}), 400

    current_user = get_jwt_identity()

    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({"code": 401, "message": "User not found"}), 401

    if user.permissions < 0:
        return jsonify({"code": 403, "message": "Permissions denied"}), 403

    photo = Photo.query.filter_by(photoid=photo_id).first()
    if not photo:
        return jsonify({"code": 404, "message": "Photo not found"}), 404

    like = Like.query.filter_by(userid=user.userid, photoid=photo_id).first()
    if not like:
        return jsonify({"code": 400, "message": "Not liked"}), 400

    db.session.delete(like)
    db.session.commit()

    return jsonify({"code": 200, "message": "Unliked successfully"}), 200

# 统计照片点赞数
def get_photo_like_count():
    photoid = request.args.get('photoid')
    if not photoid:
        return jsonify({"code": 400, "message": "photoid is required"}), 400
    try:
        like_count = Like.query.filter_by(photoid=photoid).count()

        return jsonify({
            "code": 200,
            "message": "success",
            "data": {
                "likes": like_count
            }
        }), 200
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"Internal server error: {str(e)}"
        }), 500

# 获取用户点赞的图片
def get_userlikes():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({"code": 401, "message": "User not found"}), 401
    if user.permissions < 0:
        return jsonify({"code": 403, "message": "Permissions denied"}), 403

    current_page = request.args.get('page', 1, type=int)
    per_page = request.args.get('perpage', 10, type=int)
    query = Like.query.filter_by(userid=user.userid)
    pagination = query.paginate(page=current_page, per_page=per_page, error_out=False)
    likes = pagination.items
    likes_list = []
    total_likes = pagination.total
    total_pages = ceil(total_likes / per_page)

    for like in likes:
        like_count = Like.query.filter_by(photoid=like.photoid).count()
        likes_list.append({
            'likeid': like.likeid,
            'photoid': like.photoid,
            "like_count": like_count,
            'userid': like.userid
        })
    return jsonify({
            "code": 200,
            "message": "success",
            "data": {
                "tatolAlbums": total_likes,
                "totalPages": total_pages,
                "per_page": per_page,
                "current_page": current_page,
                "likes": likes_list
            }
        })

# 评论点赞
def like_comment(usertoken):
    data = request.get_json()

    user = User.query.filter_by(usertoken=usertoken).first()
    if not user:
        return jsonify({"code": 401, "message": "Token is invalid"}), 401
    if user.permissions < 0:
        return jsonify({"code": 403, "message": "Permissions denied"}), 403
    
    comment_id = data.get("comment_id")
    if not comment_id:
        return jsonify({"code": 400, "message": "Invalid parameters"}), 400
    comment = Comment.query.filter_by(commentid=comment_id).first()
    if not comment:
        return jsonify({"code": 404, "message": "Comment not found"}), 404
    
    comment_like = CommentLike.query.filter_by(userid=usertoken, commentid=comment_id).first()
    if comment_like:
        return jsonify({"code": 400, "message": "Already liked"}), 400
    
    comment_like = CommentLike(userid=usertoken, commentid=comment_id)
    db.session.add(comment_like)
    db.session.commit()
    return jsonify({"code": 200, "message": "Liked successfully"}), 200

# 取消评论点赞
def unlike_comment(usertoken):
    data = request.get_json()

    user = User.query.filter_by(usertoken=usertoken).first()
    if not user:
        return jsonify({"code": 401, "message": "Token is invalid"}), 401
    if user.permissions < 0:
        return jsonify({"code": 403, "message": "Permissions denied"}), 403
    
    comment_id = data.get("comment_id")
    if not comment_id:
        return jsonify({"code": 400, "message": "Invalid parameters"}), 400
    comment = Comment.query.filter_by(commentid=comment_id).first()
    if not comment:
        return jsonify({"code": 404, "message": "Comment not found"}), 404
    
    comment_like = CommentLike.query.filter_by(userid=usertoken, commentid=comment_id).first()
    if not comment_like:
        return jsonify({"code": 400, "message": "Not liked"}), 400
    
    db.session.delete(comment_like)
    db.session.commit()
    return jsonify({"code": 200, "message": "Unliked successfully"}), 200

# 统计评论点赞数
def get_comment_like_count(comment_id):
    comment_likes = CommentLike.query.filter_by(commentid=comment_id).all()
    return len(comment_likes)
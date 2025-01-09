from app import db
from app.models import Photo, User, Like, Comment, CommentLike
from flask import request, jsonify

# 点赞图片
def like_photo(usertoken):
    data = request.get_json()

    user = User.query.filter_by(usertoken=usertoken).first()
    if not user:
        return jsonify({"code": 401, "message": "Token is invalid"}), 401
    if user.permissions < 0:
        return jsonify({"code": 403, "message": "Permissions denied"}), 403
    
    photo_id = data.get("photo_id")
    if not photo_id:
        return jsonify({"code": 400, "message": "Invalid parameters"}), 400
    photo = Photo.query.filter_by(photoid=photo_id).first()
    if not photo:
        return jsonify({"code": 404, "message": "Photo not found"}), 404
    
    like = Like.query.filter_by(userid=usertoken, photoid=photo_id).first()
    if like:
        return jsonify({"code": 400, "message": "Already liked"}), 400
    
    like = Like(userid=usertoken, photoid=photo_id)
    db.session.add(like)
    db.session.commit()
    return jsonify({"code": 200, "message": "Liked successfully"}), 200
    
# 取消点赞图片
def unlike_photo(usertoken):
    data = request.get_json()

    user = User.query.filter_by(usertoken=usertoken).first()
    if not user:
        return jsonify({"code": 401, "message": "Token is invalid"}), 401
    if user.permissions < 0:
        return jsonify({"code": 403, "message": "Permissions denied"}), 403
    
    photo_id = data.get("photo_id")
    if not photo_id:
        return jsonify({"code": 400, "message": "Invalid parameters"}), 400
    photo = Photo.query.filter_by(photoid=photo_id).first()
    if not photo:
        return jsonify({"code": 404, "message": "Photo not found"}), 404
    
    like = Like.query.filter_by(userid=usertoken, photoid=photo_id).first()
    if not like:
        return jsonify({"code": 400, "message": "Not liked"}), 400
    
    db.session.delete(like)
    db.session.commit()
    return jsonify({"code": 200, "message": "Unliked successfully"}), 200

# 统计图片点赞数
def get_photo_like_count(photo_id):
    likes = Like.query.filter_by(photoid=photo_id).all()
    return len(likes)

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
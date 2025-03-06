from app import db
from app.models import Photo, User, Comment
from flask import request, jsonify
from app.utils import get_utc_time

# 发表评论
def comment_photo():
    data = request.get_json()
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({"code": 401, "message": "User not found"}), 401
    if user.permissions < 0:
        return jsonify({"code": 403, "message": "Permissions denied"}), 403
    
    photo_id = data.get("photo_id")
    if not photo_id:
        return jsonify({"code": 400, "message": "Invalid parameters"}), 400
    photo = Photo.query.filter_by(photoid=photo_id).first()
    if not photo:
        return jsonify({"code": 404, "message": "Photo not found"}), 404
    
    content = data.get("content")
    if not content:
        return jsonify({"code": 400, "message": "Invalid parameters"}), 400
    
    comment = Comment(content=content, create_time=get_utc_time(), userid=usertoken, photoid=photo_id)
    db.session.add(comment)
    db.session.commit()
    return jsonify({"code": 200, "message": "Comment posted successfully", "comment": comment.to_dict()}), 200

# 删除评论
def delete_comment():
    data = request.get_json()

    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
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
    
    if comment.userid!= usertoken:
        return jsonify({"code": 403, "message": "Permissions denied"}), 403
    
    db.session.delete(comment)
    db.session.commit()
    return jsonify({"code": 200, "message": "Comment deleted successfully"}), 200

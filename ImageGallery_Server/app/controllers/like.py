from app import db
from app.models import Photo, User, Like, Comment, CommentLike
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

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
def user_likes():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({"code": 401, "message": "User not found"}), 401
    if user.permissions < 0:
        return jsonify({"code": 403, "message": "Permissions denied"}), 403

    try:
        user_likelist = Like.query.filter_by(userid=user.userid).all()
        likes_data = [like.to_dict() for like in user_likelist]

        return jsonify({
            "code": 200,
            "message": "success",
            "data": {
                "likes": likes_data 
            }
        }), 200
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"Internal server error: {str(e)}"
        }), 500
    

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
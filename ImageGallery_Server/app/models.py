from app import db
from datetime import datetime

# 用户表
class User(db.Model):
    __tablename__ = 'user'
    userid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    usertoken = db.Column(db.String(120), unique=True, nullable=False)
    permissions = db.Column(db.Integer, nullable=False)


# 相册表
class Album(db.Model):
    __tablename__ = 'album'
    albumid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False)

# 照片表
class Photo(db.Model):
    __tablename__ = 'photos'
    photoid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    desc = db.Column(db.String(500))  # 图片描述
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)
    thumbnail = db.Column(db.String(200))  # 缩略图的URL
    photo_url = db.Column(db.String(200))  # 原图的URL
    albumid = db.Column(db.Integer, db.ForeignKey('album.albumid'), nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False)

# 评论表
class Comment(db.Model):
    __tablename__ = 'comments'
    commentid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(500), nullable=False)
    create_time = db.Column(db.DateTime)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False)
    photoid = db.Column(db.Integer, db.ForeignKey('photos.photoid'), nullable=False)
    replyid = db.Column(db.Integer, nullable=False)

# 点赞表
class Like(db.Model):
    __tablename__ = 'likes'
    likeid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False)
    photoid = db.Column(db.Integer, db.ForeignKey('photos.photoid'), nullable=False)
    def to_dict(self):
        return {
            "likeid": self.likeid,
            "userid": self.userid,
            "photoid": self.photoid
        }

# 评论点赞表
class CommentLike(db.Model):
    __tablename__ = 'comment_likes'
    commentlikeid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable=False)
    commentid = db.Column(db.Integer, db.ForeignKey('comments.commentid'), nullable=False)


from flask import jsonify
from app.models import Album
from app.models import Photo, Album, User

def get_all_albums(usertoken):
    user = User.query.filter_by(usertoken=usertoken).first()
    if not user:
        return jsonify({"code": 401, "message": "token failed"}), 401
    if user.permissions < 1:
        return jsonify({"code": 403, "message": "permission denied"}), 403
    
    albums = Album.query.all()
    album_list = []
    for album in albums:
        album_list.append({
            'albumid': album.albumid,
            'name': album.name,
            "description": album.description,
            'userid': album.userid,
            'create_time': album.create_time
        })
    return jsonify({
            "code": 200,
            "message": "success",
            "data": {
                "albums": album_list
            }
        })


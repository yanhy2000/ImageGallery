from flask import jsonify
from app.models import Album

def get_all_albums():
    albums = Album.query.all()
    album_list = []
    for album in albums:
        album_list.append({
            'albumid': album.albumid,
            'name': album.name,
            'userid': album.userid,
            'create_time': album.create_time
        })
    return jsonify(album_list)

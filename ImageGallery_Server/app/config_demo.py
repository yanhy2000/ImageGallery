#文件名修改为config.py以启用
class Config:
    SQLALCHEMY_DATABASE_NAME = 'gallery.db'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{SQLALCHEMY_DATABASE_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SUPERBED_TOKEN = 'false'
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = 5000

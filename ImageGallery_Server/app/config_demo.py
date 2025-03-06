#文件名修改为config.py以启用
class Config:

    # 数据库配置
    SQLALCHEMY_DATABASE_NAME = 'gallery.db'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{SQLALCHEMY_DATABASE_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 是否保存原图
    SAVE_ORIGINAL_IMAGE = True

    # 调试模式
    DEBUG = True

    # 服务器配置
    HOST = '0.0.0.0'
    PORT = 5000
#文件名修改为config.py以启用
class Config:

    # 数据库配置
    SQLALCHEMY_DATABASE_NAME = 'gallery.db'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{SQLALCHEMY_DATABASE_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #Token\密钥类型,可选Token\Password
    #该项仅在初始化时生效，取决于项目运作方式，如不开放注册仅由管理员发放token则推荐选Token类型，每个用户以Token鉴权
    #如作为开放社区开放自由注册建议改为Password、
    #功能开发中，目前以token为主导
    Token_Type = Token

    # 是否保存原图
    SAVE_ORIGINAL_IMAGE = True

    # 是否开放注册，不开放仅由后台新建用户
    ENABLE_REGISTER = True
    
    # JWT密钥配置
    JWT_SECRET_KEY = "jwt-secret"

    # 调试模式
    DEBUG = True

    # 服务器配置
    HOST = '0.0.0.0'
    PORT = 5000
from app import app
from app.config import Config
import os

if __name__ == '__main__':
    # 初始化数据库
    try:
        if not os.path.exists(f"./instance/{Config.SQLALCHEMY_DATABASE_NAME}"):
            print('数据库不存在, 请手动运行 python init_db.py')
            exit()
    except Exception as e:
        print(f'数据库不存在或连接失败, 请检查数据库配置:{e}')
        exit()
    
    try:
        if not os.path.exists("./ssl"):
            print('ssl证书不存在, 将使用http协议')
            print("如需使用https协议, 请将ssl证书放置在ssl目录下, 分别为fullchain.pem和privkey.key")
            app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT)
        else:
            print('ssl证书存在, 将使用https协议')
            context = ('ssl/fullchain.pem', 'ssl/privkey.key')
            app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT, ssl_context=context)
    except Exception as e:
        print(f'启动异常:{e}')

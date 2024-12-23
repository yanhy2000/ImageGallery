from app import app
from app.config import Config
import os

if __name__ == '__main__':
    # 初始化数据库
    try:
        if not os.path.exists(f"./instance/{Config.SQLALCHEMY_DATABASE_NAME}"):
            print({Config.SQLALCHEMY_DATABASE_NAME})
            print('数据库不存在，请手动运行 python init_db.py')
            exit()
    except Exception as e:
        print(f'数据库不存在或连接失败，请检查数据库配置:{e}')
        exit()
    app.run(debug=True)

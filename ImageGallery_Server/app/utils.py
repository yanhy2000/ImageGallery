import uuid
import os
# 用于生成文件的UUID
def generate_uuid_filename():
    return str(uuid.uuid4())

# 用于生成用户的token
def generate_user_uuid():
    return str(uuid.uuid4())

# 获取项目根目录路径
def get_project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
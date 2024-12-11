import uuid

# 用于生成文件的UUID
def generate_uuid_filename():
    return str(uuid.uuid4())

# 用于生成用户的token
def generate_user_uuid():
    return str(uuid.uuid4())
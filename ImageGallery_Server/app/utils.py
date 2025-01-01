import uuid
import os
from datetime import datetime, timezone
from pytz import timezone

def get_utc_time():
    return datetime.now(timezone('Asia/Shanghai'))

# 将 UTC 转换为本地时间
def utc_to_local(utc_dt):
    local_tz = timezone('Asia/Shanghai')
    return utc_dt.astimezone(local_tz)


# 用于生成文件的UUID
def generate_uuid_filename():
    return str(uuid.uuid4())

# 用于生成用户的token
def generate_user_uuid():
    return str(uuid.uuid4())

# 获取项目根目录路径
def get_project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


import os
import requests
import json

def main():
    print("脚本运行...")

    base_url = input("请输入您的ImageGallery站点后端地址(如：http://localhost)：").strip()
    if not base_url.startswith(('http://', 'https://')):
        base_url = 'http://' + base_url
    base_url = base_url.rstrip('/')
    usertoken = input("请输入您的用户Token并回车: ").strip()
    
    try:
        file_path = input("请输入您要上传的照片路径并回车（可直接拖入cmd窗口内）：").strip('"\' ')
        print("正在检查文件是否有效...")
        
        if not os.path.exists(file_path):
            print("文件不存在！")
            return
            
        if os.path.getsize(file_path) == 0:
            print("文件大小为0，无效文件！")
            return
            
        print("文件有效！")
        
        desc = input("请输入关于这张图片的描述（可选，直接回车则使用'无描述'）：").strip()
        if not desc:
            desc = "无描述"
            
        album = input("请输入存放这张图片的相册（可选，直接回车则使用 noalbum 作为相册）：").strip()
        if not album:
            album = "noalbum"
            print(f"将使用 noalbum 作为相册名称")
        
        print("开始上传...")
        try:
            with open(file_path, 'rb') as f:
                files = {
                    'file': (os.path.basename(file_path), f, 'image/jpeg')
                }
                data = {
                    'desc': desc,
                    'album': album
                }
                headers = {
                    'Authorization': f'Bearer {usertoken}'
                }
                
                upload_response = requests.post(
                    f"{base_url}/api/upload",
                    headers=headers,
                    files=files,
                    data=data
                )
                
                if upload_response.status_code == 200:
                    print("上传成功！")
                    print(f"返回数据: {upload_response.json()}")
                else:
                    print(f"上传失败！原因：{upload_response.json().get('message', '未知错误')}")
                    
        except Exception as e:
            print(f"上传过程中发生错误: {str(e)}")
            
    except requests.exceptions.RequestException as e:
        print(f"网络请求错误: {str(e)}")
    except Exception as e:
        print(f"发生未知错误: {str(e)}")

if __name__ == "__main__":
    main()
# 照片管理API文档

## 1. 获取公开照片列表 (GET /api/photos)

**描述**：获取公开的照片列表（分页展示）

**请求**：
* **URL**：`/api/photos`
* **方法**：`GET`
* **认证**：不需要

**请求头**：

* `Content-Type: application/json`


**参数**：
* **查询参数**：
  * `page`: 当前页码（默认1）
  * `perpage`: 每页数量（默认10）

**返回示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "totalPhotos": 100,
    "totalPages": 10,
    "per_page": 10,
    "current_page": 1,
    "photos": [
      {
        "photoid": 1,
        "desc": "美丽的风景",
        "upload_time": "2023-05-20 12:00:00",
        "upload_user": "user1",
        "thumbnail": "/uploads/thumbnails/abc123.jpg",
        "likes": 15
      }
    ]
  }
}
```

---

## 2. 获取管理照片列表 (GET /api/admin/photos)

**描述**：管理员获取所有照片列表（需要权限）

**请求**：
* **URL**：`/api/admin/photos`
* **方法**：`GET`
* **认证**：需要`usertoken`
* **权限**：`permissions >= 1`

**请求头**：

* `Content-Type: application/json`
* `Authorization: Bearer <usertoken>`

**参数**：
* **查询参数**：
  * `page`: 当前页码（默认1）
  * `perpage`: 每页数量（默认10）

**返回示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "totalPhotos": 100,
    "totalPages": 10,
    "per_page": 10,
    "current_page": 1,
    "photos": [
      {
        "photoid": 1,
        "name": "sunset.jpg",
        "desc": "日落照片",
        "upload_time": "2023-05-20 12:00:00",
        "thumbnail": "/uploads/thumbnails/abc123.jpg",
        "photo_url": "/uploads/original/abc123.jpg",
        "album_name": "旅行相册",
        "albumid": 1,
        "userid": 1,
        "username": "user1"
      }
    ]
  }
}
```

---

## 3. 上传照片 (POST /api/upload)

**描述**：上传新照片

**请求**：
* **URL**：`/api/upload`
* **方法**：`POST`
* **认证**：需要`usertoken`
* **权限**：`permissions >= 0`

**请求头**：

  * `Content-Type: multipart/form-data`
  * `Authorization: Bearer <usertoken>`

**请求体示例**：

```
--Boundary
Content-Disposition: form-data; name="file"; filename="example.jpg"
Content-Type: image/jpeg
[图片二进制数据]
--Boundary
Content-Disposition: form-data; name="desc"
图片描述
--Boundary
Content-Disposition: form-data; name="album"
相册名称
--Boundary--
```

**参数**：
* **表单数据**：
  * `file`: 图片文件（必填）
  * `name`: 图片名称（可选，默认使用文件名）
  * `desc`: 图片描述（可选，默认"无描述"）
  * `album`: 相册名称（可选，默认使用用户名）

**返回示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": 5  // 新照片ID
}
```

---

## 4. 删除照片 (DELETE /api/photos)

**描述**：删除指定照片

**请求**：
* **URL**：`/api/photos`
* **方法**：`DELETE`
* **认证**：需要`usertoken`

**请求头**：

* `Content-Type: application/json`
* `Authorization: Bearer <usertoken>`

**参数**：
* **请求体**：
  ```json
  {
    "photoid": 1
  }
  ```

**返回示例**：
```json
{
  "code": 200,
  "message": "Photo deleted successfully"
}
```

---

## 5. 获取照片文件 (GET /api/photos/{photoid}/file)

**描述**：下载照片文件（可获取缩略图）

**请求**：
* **URL**：`/api/photos/{photoid}/file`
* **方法**：`GET`
* **认证**：不需要

**参数**：
* **查询参数**：
  * `thumbnail`: 是否获取缩略图（1=是，0=否，默认1）

**返回**：
* 图片二进制数据（Content-Type: image/jpeg 或 image/png）

---

## 6. 获取照片信息 (GET /api/photos/{photoid})

**描述**：获取照片详细信息（公开版）

**请求**：
* **URL**：`/api/photos/{photoid}`
* **方法**：`GET`
* **认证**：不需要

**请求头**：

* `Content-Type: application/json`

**返回示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "photoid": 1,
    "name": "sunset.jpg",
    "desc": "美丽的日落",
    "upload_time": "2023-05-20 12:00:00",
    "uploader": "user1",
    "thumbnail": "/uploads/thumbnails/abc123.jpg",
    "photo_url": "/uploads/original/abc123.jpg",
    "albumname": "旅行相册",
    "userid": 1
  }
}
```

---

## 7. 获取照片完整信息 (GET /api/photos/{photoid}/full)

**描述**：获取照片完整信息（需要权限）

**请求**：
* **URL**：`/api/photos/{photoid}/full`
* **方法**：`GET`
* **认证**：需要`usertoken`
* **权限**：照片所有者或管理员

**请求头**：

* `Content-Type: application/json`
* `Authorization: Bearer <usertoken>`

**返回示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "photoid": 1,
    "name": "sunset.jpg",
    "desc": "美丽的日落",
    "upload_time": "2023-05-20 12:00:00",
    "thumbnail": "/uploads/thumbnails/abc123.jpg",
    "photo_url": "/uploads/original/abc123.jpg",
    "albumname": "旅行相册",
    "userid": 1
  }
}
```

---

## 8. 更新照片信息 (PUT /api/photos/{photoid})

**描述**：更新照片信息

**请求**：
* **URL**：`/api/photos/{photoid}`
* **方法**：`PUT`
* **认证**：需要`usertoken`
* **权限**：照片所有者或管理员

**请求头**：

* `Content-Type: application/json`
* `Authorization: Bearer <usertoken>`

**参数**：
* **请求体**：
  ```json
  {
    "name": "新名称",
    "desc": "新描述",
    "albumid": 2
  }
  ```

**返回示例**：
```json
{
  "code": 200,
  "message": "Photo updated successfully"
}
```

## 特殊说明

1. **缩略图生成规则**：
   - 自动生成900x900像素的缩略图
   - 存储路径：`uploads/.thumbnails/`
   - 格式统一转换为JPEG

2. **文件存储结构**：
   ```
   uploads/
   ├── 2023/
   │   ├── 05/
   │   │   ├── 20/
   │   │   │   ├── original1.jpg
   ├── .thumbnails/
   │   ├── thumb1.jpg
   ```

3. **权限控制**：
   - 公开接口：无需认证
   - 用户接口：`permissions >= 0`
   - 管理接口：`permissions >= 1`
```
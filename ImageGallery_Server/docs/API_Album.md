# 相册管理接口文档

## 1. 获取所有相册列表 (GET /api/albums)

**描述**：获取系统中的所有相册列表（分页展示，需要管理员权限）

**请求**：
* **URL**：`/api/albums`
* **方法**：`GET`
* **认证**：需要`usertoken`
* **权限**：`permissions >= 1`（管理员）

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
    "totalAlbums": 15,
    "totalPages": 2,
    "per_page": 10,
    "current_page": 1,
    "albums": [
      {
        "albumid": 1,
        "name": "旅行相册",
        "userid": 1,
        "create_time": "2023-05-20 12:00:00"
      }
    ]
  }
}
```

---

## 2. 创建相册 (POST /api/albums)

**描述**：创建新相册（需要管理员权限）

**请求**：
* **URL**：`/api/albums`
* **方法**：`POST`
* **认证**：需要`usertoken`
* **权限**：`permissions >= 1`

**请求头**：

* `Content-Type: application/json`
* `Authorization: Bearer <usertoken>`

**参数**：
* **请求体**：
  ```json
  {
    "name": "新相册名称"
  }
  ```

**返回示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "albumid": 5  // 新创建的相册ID
  }
}
```

**错误响应**：
- 400：缺少必要参数
- 401：Token无效
- 403：权限不足

---

## 3. 删除相册 (DELETE /api/albums)

**描述**：删除指定相册及其包含的所有照片（需要管理员权限）

**请求**：
* **URL**：`/api/albums`
* **方法**：`DELETE`
* **认证**：需要`usertoken`
* **权限**：`permissions >= 1`

**请求头**：

* `Content-Type: application/json`
* `Authorization: Bearer <usertoken>`

**参数**：
* **请求体**：
  ```json
  {
    "albumid": 1
  }
  ```

**返回示例**：
```json
{
  "code": 200,
  "message": "success"
}
```

**特殊说明**：
- 会级联删除相册下的所有照片
- 同时会删除服务器上的照片文件

---

## 4. 修改相册信息 (PUT /api/albums)

**描述**：修改相册名称（需要管理员权限）

**请求**：
* **URL**：`/api/albums`
* **方法**：`PUT`
* **认证**：需要`usertoken`
* **权限**：`permissions >= 1`

**请求头**：

* `Content-Type: application/json`
* `Authorization: Bearer <usertoken>`

**参数**：
* **请求体**：
  ```json
  {
    "albumid": 1,
    "name": "新相册名称"
  }
  ```

**返回示例**：
```json
{
  "code": 200,
  "message": "success"
}
```

**错误响应**：
- 400：缺少必要参数或没有修改内容
- 404：相册不存在

---

## 5. 获取用户自己的相册列表 (GET /api/user_albums)

**描述**：获取用户自己的相册列表（分页展示）

**请求**：
* **URL**：`/api/user_albums`
* **方法**：`GET`
* **认证**：需要`usertoken`
* **权限**：`permissions >= 0`

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
    "totalAlbums": 15,
    "totalPages": 2,
    "per_page": 10,
    "current_page": 1,
    "albums": [
      {
        "albumid": 1,
        "name": "旅行相册",
        "create_time": "2023-05-20 12:00:00"
      }
    ]
  }
}
```

---

## 安全说明

1. **权限验证**：
   - 所有管理接口都需要有效的`usertoken`
   - 需要管理员权限（`permissions >= 1`）

2. **数据完整性**：
   - 删除相册时会同步删除关联的照片记录和文件
   - 修改操作会验证相册是否存在

3. **请求验证**：
   - 所有修改操作都会验证必要参数
   - 会检查相册是否存在

## 最佳实践建议

1. 前端应在删除相册前显示确认对话框
2. 修改相册名称时应检查名称是否已存在
3. 获取相册列表时可配合获取相册下的照片数量信息
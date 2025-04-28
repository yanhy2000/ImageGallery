# 数据库设计
## 数据库结构设计

数据库类型：sqlite

## 数据库表

| photos                 | user        | album               |
| ------------------------ | ------------- | --------------------- |
| photoid                | userid      | albumid             |
| name                   | username    | name                |
| desc                   | usertoken   | userid |
| upload_time            | permissions | create_time         |
| thumbnail              |             |                     |
| photo_url              |             |                     |
| albumid                |             |                     |
| userid                 |             |                     |


## 后端接口设计

# 图片

## 下载图片（Get /api/getphoto）

**描述**：用于获取图片文件。此操作不需要身份验证。

**请求**：

* **URL**：`/api/getphoto`
* **方法**：`GET`

**参数**：

* **查询参数**：

  * `photoid`: 图片唯一值ID（必填）
  * `thumbnail`: 是否为缩略图，默认为True（可选）

  **示例：**
* ```url
  http://127.0.0.1:5000/api/getphoto?photoid=1&thumbnail=false
  ```

**返回**：

* **格式**：`image/jpeg` 或 `image/png`（根据图片类型）
* **内容**：图片文件的二进制数据

---

## 上传图片（Post /api/upload）

**描述**：用户通过此端点上传图片，并在上传时需要提供 `usertoken` 进行身份验证。

**请求**：

* **URL**：`/api/upload`
* **方法**：`POST`
* **请求头**：

  * `Content-Type: multipart/form-data`
  * `Authorization: Bearer <usertoken>`

**参数**：

* **载荷**：包含图片文件和其他图片信息。

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

**返回**：

* **格式**：`application/json`
* **示例**：

```json
{
  "code": 200,
  "message": "success",
  "data": "photoid"
}
```

---

## 删除图片（POST /api/deletephoto）

**描述**：用户通过此端点删除特定图片，需要提供 `usertoken` 进行身份验证。

**请求**：

* **URL**：`/api/deletephoto`
* **方法**：`POST`
* **请求头**：

  * `Content-Type: application/json`
  * `Authorization: Bearer <usertoken>`

**参数**：

* **路径参数**：

  * `photoid`: 图片的唯一标识符

```json
{
	"photoid": 1
}
```

**返回**：

* **格式**：`application/json`
* **示例**：

```json
{
  "code": 200,
  "message": "Photo deleted successfully"
}
```

---

## 获取图片信息（Get /api/getphotoinfo_all）

**描述**：用于获取图片信息。需要提供 `usertoken` 进行身份验证。

**请求**：

* **URL**：`/api/getphotoinfo_all`
* **方法**：`GET`
* **请求头**：

  * `Content-Type: application/json`
  * `Authorization: Bearer <usertoken>`

**参数**：

* **查询参数**：

  * `photoid`: 图片唯一值ID（必填）
* 示例：

  ```url
  curl -X GET http://127.0.0.1:5000/api/getphotoinfo_all?photoid=1 -H "Authorization: Bearer 254d4299-354d-4f51-ab62-9b3da50a73e9"
  ```

**返回**：

* **格式**：`application/json`
* **示例**：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "photoid": "abcdefg",
    "name": "phname",
    "desc": "this is a photo",
    "upload_time": "2021-01-01 12:00:00",
    "small_url": "https://cdn.example.com/small/abcdefg.jpg",
    "large_url": "https://cdn.example.com/large/abcdefg.jpg",
    "album": "albumname",
    "user_id": 123456
  }
}
```

---

## 获取图片公开展示信息（Get /api/getphotoinfo）

**描述**：用于获取图片信息。无需进行身份验证。

**请求**：

* **URL**：`/api/getphotoinfo`
* **方法**：`GET`
* **请求头**：

  * `Content-Type: application/json`

**参数**：

* **查询参数**：

  * `photoid`: 图片唯一值ID（必填）
* 示例：

  ```url
  curl -X GET http://127.0.0.1:5000/api/getphotoinfo?photoid=1
  ```

**返回**：

* **格式**：`application/json`
* **示例**：

```json
{
  "code": 200,
  "data": {
    "desc": "无描述",
    "name": "photo test",
    "photo_url": "uploads\\12\\11\\f8fca309-7b55-4d62-98a4-fc2cbf786954.jpg",
    "photoid": 1,
    "thumbnail": "https://pic.xx/a.jpg",
    "upload_time": "2024-12-11 02:58:39",
    "uploader": "admin",
    "userid": 1
  },
  "message": "success"
}
```

---

## 获取全部图片列表（Get /api/photos_list）

**描述**：用于获取图片列表。无需进行身份验证。

**请求**：

* **URL**：`/api/photos_list`
* **方法**：`GET`
* **请求头**：

  * `Content-Type: application/json`

**参数**：

* **查询参数**：

  * `page`: 当前页数(可选)
  * `perpage`: 每页数量(可选)
* 示例：

  ```url
  curl -X GET http://127.0.0.1:5000/api/photos_list?page=1&perpage=10
  ```

**返回**：

* **格式**：`application/json`
* **示例**：

```json
{
  "code": 200,
  "data": {
    "current_page": 1,
    "per_page": 10,
    "photos": [
      {
        "desc": "无描述",
        "photoid": 1,
        "thumbnail": "https://pic.xx/a.jpg",
        "upload_time": "2024-12-11 02:58:39",
        "upload_user": "admin"
      }
    ],
    "total": 1
  },
  "message": "success"
}
```
---

## 获取图片详细信息列表（Post /api/photolist）

**描述**：用于获取图片列表,需要提供 `usertoken` 进行身份验证。

**请求**：

* **URL**：`/api/photolist`
* **方法**：`POST`
* **请求头**：

  * `Content-Type: application/json`
  * `Authorization: Bearer <usertoken>`

**参数**：

* **载荷**：包含分页信息。

**请求体示例**：

```json
{
	"page": 1,
	"perpage": 10
}
```

**返回**：

* **格式**：`application/json`
* **示例**：

```json
{
  "code": 200,
  "data": {
    "current_page": 1,
    "per_page": 10,
    "photos": [
      {
        "desc": "无描述",
        "photoid": 1,
        "thumbnail": "https://pic.xx/a.jpg",
        "upload_time": "2024-12-11 02:58:39",
        "upload_user": "admin"
      }
    ],
    "total": 1
  },
  "message": "success"
}
```

---

## 更新图片信息（POST /api/updatephoto）

**描述**：用户通过此端点更新图片的名称、描述或所属相册，需要提供 `usertoken` 进行身份验证。

**请求**：

* **URL**：`/api/updatephoto`
* **方法**：`POST`
* **请求头**：

  * `Content-Type: application/json`
  * `Authorization: Bearer <usertoken>`

**参数**：

* **载荷**：包含要更新的字段，需要至少传入`photoid`，其余为空则不更新。

  **请求体示例**：

  ```json
  {
    "photoid": 1,
    "name": "新的图片名称",
    "desc": "新的图片描述",
    "album": "新的相册名称"
  }
  ```

**返回**：

* **格式**：`application/json`
* **示例**：

```json
{
  "code": 200,
  "message": "Photo information updated successfully"
}
```

---


# 用户

## 新增用户（Post /api/adduser）

**描述**：管理员通过此端点新增用户，并在创建成功后获取用户token。需要提供 `usertoken` 进行身份验证。

**请求**：

* **URL**：`/api/adduser`
* **方法**：`POST`

**请求头**：

* `Content-Type: application/json`
* `Authorization: Bearer <usertoken>`

**参数**：

* **载荷**：包含用户名信息。

**请求体示例**：

```json
{
  "name": "新的用户名"
}
```

**返回**：

* **格式**：`application/json`
* **示例**：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "userid": "123456",
	"username": "aaa",
	"permissions": 1,
	"token": "aabbcc"
  }
}
```

---

## 删除用户（Post /api/deluser）

**描述**：管理员通过此端点删除用户。需要提供 `usertoken` 进行身份验证。

**请求**：

* **URL**：`/api/deluser`
* **方法**：`POST`

**请求头**：

* `Content-Type: application/json`
* `Authorization: Bearer <usertoken>`

**参数**：

* **载荷**：包含用户名、用户ID信息。

**请求体示例**：

```json
{
	"userid": 123,
	"name": "用户名"
}
```

**返回**：

* **格式**：`application/json`
* **示例**：

```json

{
  "code": 200,
  "message": "success",
  "data": {
	"deluser": "aaa",
  }
}
```

---

## 修改用户（Post /api/setuser）

**描述**：管理员通过此端点修改用户，可选择修改用户权限、用户名、token等。需要提供 `usertoken` 进行身份验证。

**请求**：

* **URL**：`/api/setuser`
* **方法**：`POST`

**请求头**：

* `Content-Type: application/json`
* `Authorization: Bearer <usertoken>`

**参数**：

* **载荷**：包含用户名、用户ID信息，以及要修改的内容，留空则为不修改。

**请求体示例**：

```json
{
	"userid": 123,
	"name": "用户名",
	"set_permissions": 0,
	"set_name": "",
	"regen_token": False
}
```

**返回**：

* **格式**：`application/json`
* **示例**：

```json

{
  "code": 200,
  "message": "success",
  "data": {
    "userid": "123456",
	"username": "aaa",
	"permissions": 1,
	"token": "aabbcc"
  }
}
```

---

## 获取用户名（Get /api/getusername）

**描述**：用于获取用户的用户名。需要提供 `usertoken` 进行身份验证。

**请求**：

* **URL**：`/api/getusername`
* **方法**：`GET`

**请求头**：

* `Content-Type: application/json`
* `Authorization: Bearer <usertoken>`

**参数**：

* `userid`: 用户ID（必填）
* 示例：

  ```url
  curl -X GET http://127.0.0.1:5000/api/getusername?userid=1 -H "Authorization: Bearer 254d4299-354d-4f51-ab62-9b3da50a73e9"
  ```

**返回**：

* **格式**：`application/json`
* **示例**：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "username": "testuser123"
  }
}
```
---
## 获取用户列表（POST /api/userlist）
**描述**：管理员通过此端点获取用户列表。需要提供 `usertoken` 进行身份验证。
**请求**：

* **URL**：`/api/userlist`
* **方法**：`POST`

**请求头**：

* `Content-Type: application/json`
* `Authorization: Bearer <usertoken>`

**参数**：

* **载荷**：无

**请求体示例**：

```json
{
	"page": 1,
	"perpage": 10
}
```

**返回**：

* **格式**：`application/json`
* **示例**：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "current_page": 1,
    "per_page": 10,
    "users": [
      {
        "userid": "123456",
        "username": "testuser123",
        "permissions": 1
      },
      // ...更多用户
    ],
    "total": 10
  }
}
```
---
## 获取相册列表（Post /api/albumlist）

**描述**：管理员通过此端点获取相册列表。需要提供 `usertoken` 进行身份验证。

**请求**：

* **URL**：`/api/albumlist`
* **方法**：`POST`

**请求头**：

* `Content-Type: application/json`
* `Authorization: Bearer <usertoken>`

**参数**：

* **载荷**：无

**请求体示例**：

```json
{
	"page": 1,
	"perpage": 10
}
```

**返回**：

* **格式**：`application/json`
* **示例**：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "current_page": 1,
    "per_page": 10,
    "albums": [
      {
        "album_id": "相册唯一标识符",
        "album_name": "相册名称",
        "description": "相册描述"
      },
      // ...更多相册
    ],
    "total": 10
  }
}
```
---
# 相册

### 创建/更新相册（Post /api/album）

**描述**：允许用户创建新的相册或更新相册信息。需要提供 `usertoken` 进行身份验证。

**请求**：

* **URL**：`/api/album`
* **方法**：`POST`
* **请求头**：

  * `Content-Type: application/json`
  * `Authorization: Bearer <usertoken>`
    **载荷**：

```json
{
  "album_name": "相册名称",
  "description": "相册描述" // 可选
}
```

**返回**：

* **格式**：`application/json`
* **示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "album_id": "相册唯一标识符",
    "album_name": "相册名称",
    "description": "相册描述"
  }
}
```

---

### 删除相册（DELETE /api/album）

**描述**：允许用户删除自己创建的相册。需要提供 `usertoken` 进行身份验证。

**请求**：

* **URL**：`/api/album`
* **方法**：`DELETE`
* **请求头**：

  * `Authorization: Bearer <usertoken>`

**参数**：

* **查询参数**：

  * `album_id`: 相册唯一标识符（可选）
  * `album_name`: 相册名称（可选）

**返回**：

* **格式**：`application/json`
* **示例**：

```json
{
  "code": 200,
  "message": "相册删除成功"
}
```

---

### 获取用户相册列表（GET /api/getalbums）

**描述**：返回用户的所有相册列表。如果提供了 `username`，则返回特定用户的相册列表。需要提供 `usertoken` 进行身份验证。

**请求**：

* **URL**：`/api/getalbums`
* **方法**：`GET`
* **请求头**：

  * `Authorization: Bearer <usertoken>`

**参数**：

* **查询参数**：

  * `username`: 用户名（可选）

**返回**：

* **格式**：`application/json`
* **示例**：

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "album_id": "相册唯一标识符",
      "album_name": "相册名称",
      "description": "相册描述"
    },
    // ...更多相册
  ]
}
```

---

### 获取相册中的图片列表（GET /api/getphotosbyalbum）

**描述**：返回指定相册中的所有图片。需要提供 `usertoken` 进行身份验证。

**请求**：

* **URL**：`/api/getphotosbyalbum`
* **方法**：`GET`
* **请求头**：

  * `Authorization: Bearer <usertoken>`

**参数**：

* **查询参数**：

  * `album_id`: 相册唯一标识符（可选）
  * `album_name`: 相册名称（可选）

**返回**：

* **格式**：`application/json`
* **示例**：

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "photoid": "图片唯一标识符",
      "name": "图片名称",
      "desc": "图片描述",
      "upload_time": "上传时间",
      "small_url": "缩略图URL",
      "large_url": "原图URL",
      "album": "相册名称",
      "user_id": "用户ID"
    },
    // ...更多图片
  ]
}
```

---

### 获取用户权限状态（GET /api/checktoken）

**描述**：返回该用户的权限状态，可以用于判断能否登录。

**请求**：

* **URL**：`/api/checktoken`
* **方法**：`GET`

**参数**：

* **查询参数**：

  * `username`: 用户名（必填）
  * `usertoken`: 用户token（必填）

**返回**：

* **格式**：`application/json`
* **示例**：

```json
{
  "code": 200,
  "message": "success",
  "data": {
      "allowlogin": True
    }
}
```

# 待更新
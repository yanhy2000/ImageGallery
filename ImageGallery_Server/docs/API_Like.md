# 点赞管理接口文档

## 1. 照片点赞 (POST /api/photos/likes)

**描述**：为指定照片点赞

**请求**：
* **URL**：`/api/photos/likes`
* **方法**：`POST`
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
  "message": "Liked successfully"
}
```

**错误响应**：
- 400：已点赞或缺少photoid
- 401：用户未认证
- 403：权限不足
- 404：照片不存在

---

## 2. 取消照片点赞 (DELETE /api/photos/likes)

**描述**：取消对指定照片的点赞

**请求**：
* **URL**：`/api/photos/likes`
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
  "message": "Unliked successfully"
}
```

**错误响应**：
- 400：未点赞或缺少photoid
- 401：用户未认证
- 403：权限不足
- 404：照片不存在

---

## 3. 获取照片点赞数 (GET /api/photos/likes/count)

**描述**：获取指定照片的点赞数量

**请求**：
* **URL**：`/api/photos/likes/count`
* **方法**：`GET`
* **认证**：不需要

**请求头**：

* `Content-Type: application/json`

**参数**：
* **查询参数**：
  * `photoid`: 照片ID（必填）

**返回示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "likes": 15
  }
}
```

---

## 4. 获取用户点赞列表 (GET /api/users/likes)

**描述**：获取当前用户点赞过的所有照片

**请求**：
* **URL**：`/api/users/likes`
* **方法**：`GET`
* **认证**：需要`usertoken`

**请求头**：

* `Content-Type: application/json`
* `Authorization: Bearer <usertoken>`


**返回示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "likes": [
      {
        "likeid": 1,
        "userid": 1,
        "photoid": 1
      }
    ]
  }
}
```

**错误响应**：
- 401：用户未认证
- 403：权限不足

---

## 5. 评论点赞 (POST /api/comments/likes)

**描述**：为指定评论点赞

**请求**：
* **URL**：`/api/comments/likes`
* **方法**：`POST`
* **认证**：需要`usertoken`

**请求头**：

* `Content-Type: application/json`
* `Authorization: Bearer <usertoken>`

**参数**：
* **请求体**：
  ```json
  {
    "comment_id": 1
  }
  ```

**返回示例**：
```json
{
  "code": 200,
  "message": "Liked successfully"
}
```

**错误响应**：
- 400：已点赞或缺少comment_id
- 401：Token无效
- 403：权限不足
- 404：评论不存在

---

## 6. 取消评论点赞 (DELETE /api/comments/likes)

**描述**：取消对指定评论的点赞

**请求**：
* **URL**：`/api/comments/likes`
* **方法**：`DELETE`
* **认证**：需要`usertoken`

**请求头**：

* `Content-Type: application/json`
* `Authorization: Bearer <usertoken>`

**参数**：
* **请求体**：
  ```json
  {
    "comment_id": 1
  }
  ```

**返回示例**：
```json
{
  "code": 200,
  "message": "Unliked successfully"
}
```

**错误响应**：
- 400：未点赞或缺少comment_id
- 401：Token无效
- 403：权限不足
- 404：评论不存在

---

## 7. 获取评论点赞数 (GET /api/comments/likes/count)

**描述**：获取指定评论的点赞数量

**请求**：
* **URL**：`/api/comments/likes/count?comment_id=1`
* **方法**：`GET`
* **认证**：不需要

**请求头**：

* `Content-Type: application/json`

**参数**：
* **查询参数**：
  * `comment_id`: 评论ID（必填）

**返回**：
* 点赞数量（整数）

---

## 权限说明

| 操作 | 所需权限 |
|------|----------|
| 照片点赞/取消 | 普通用户(permissions >= 0) |
| 评论点赞/取消 | 普通用户(permissions >= 0) |
| 获取点赞数据 | 公开或需认证(视情况而定) |

## 数据关系

1. **用户-照片点赞**：一对多关系
2. **用户-评论点赞**：一对多关系
3. **照片-点赞**：一对多关系
4. **评论-点赞**：一对多关系
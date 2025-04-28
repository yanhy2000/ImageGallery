# 用户管理接口文档

## 1. 获取所有用户列表 (GET /api/users)

**描述**：获取系统中的所有用户列表（分页展示，需要管理员权限）

**请求**：
* **URL**：`/api/users`
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
    "users": [
      {
        "userid": 1,
        "username": "admin",
        "permissions": 1,
        "usertoken": "xxxxx-xxxx-xxxx"
      }
    ],
    "per_page": 10,
    "current_page": 1,
    "totalUsers": 15,
    "totalPages": 2
  }
}
```

---

## 2. 添加新用户 (POST /api/users)

**描述**：创建新用户（需要管理员权限）

**请求**：
* **URL**：`/api/users`
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
    "name": "newuser"
  }
  ```

**返回示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "userid": 5,
    "username": "newuser",
    "usertoken": "xxxxx-xxxx-xxxx"
  }
}
```

**错误响应**：
- 400：用户名已存在或缺少用户名
- 401：Token无效
- 403：权限不足

---

## 3. 获取用户名 (GET /api/users/{userid})

**描述**：获取指定用户的用户名（需要管理员权限）

**请求**：
* **URL**：`/api/users/{userid}`
* **方法**：`GET`
* **认证**：需要`usertoken`
* **权限**：`permissions >= 1`

**请求头**：

* `Content-Type: application/json`
* `Authorization: Bearer <usertoken>`

**返回示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "username": "testuser"
  }
}
```

---

## 4. 删除用户 (DELETE /api/users)

**描述**：删除指定用户（需要管理员权限）

**请求**：
* **URL**：`/api/users`
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
    "userid": 1,
    "name": "confirm_username"
  }
  ```

**返回示例**：
```json
{
  "code": 200,
  "message": "success"
}
```

**安全机制**：
- 需要确认用户名匹配才能删除
- 防止误删除操作

---

## 5. 修改用户信息 (PUT /api/users)

**描述**：修改用户信息（需要管理员权限）

**请求**：
* **URL**：`/api/users`
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
    "userid": 1,
    "name": "current_username",
    "set_name": "new_username",
    "set_permissions": 1,
    "regen_token": true
  }
  ```

**返回示例**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "userid": 1,
    "username": "new_username",
    "permissions": 1,
    "usertoken": "new_generated_token"
  }
}
```

**可修改项**：
- 用户名
- 权限等级
- 重新生成用户Token

---

## 权限等级说明

| 等级 | 说明 |
|------|------|
| -2 | 已删除用户 |
| 0 | 普通用户 |
| 1 | 管理员 |

## 安全注意事项

1. **Token安全**：
   - 用户Token相当于密码，应妥善保管
   - 可通过`regen_token`参数强制刷新Token

2. **删除保护**：
   - 删除用户需要确认用户名
   - 已删除用户标记为权限等级-2

3. **权限控制**：
   - 所有管理接口都需要管理员权限
   - 管理员不能修改自己的权限等级

4. **审计日志建议**：
   - 记录所有用户管理操作
   - 特别是删除和权限变更操作
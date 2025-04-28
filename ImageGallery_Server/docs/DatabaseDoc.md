# 数据库设计文档

## 数据库结构设计

### 数据库类型
- SQLite

### 数据表结构

#### 1. 用户表 (user)
| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| userid | Integer | PRIMARY KEY, AUTO_INCREMENT | 用户唯一标识 |
| username | String(80) | UNIQUE, NOT NULL | 用户名 |
| usertoken | String(120) | UNIQUE, NOT NULL | 用户认证令牌 |
| permissions | Integer | NOT NULL | 用户权限等级 |

#### 2. 相册表 (album)
| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| albumid | Integer | PRIMARY KEY, AUTO_INCREMENT | 相册唯一标识 |
| name | String(120) | NOT NULL | 相册名称 |
| create_time | DateTime | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| userid | Integer | FOREIGN KEY(user.userid), NOT NULL | 所属用户ID |

#### 3. 照片表 (photos)
| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| photoid | Integer | PRIMARY KEY, AUTO_INCREMENT | 照片唯一标识 |
| name | String(120) | NOT NULL | 照片名称 |
| desc | String(500) |  | 照片描述（可选） |
| upload_time | DateTime | DEFAULT CURRENT_TIMESTAMP | 上传时间 |
| thumbnail | String(200) |  | 缩略图URL |
| photo_url | String(200) |  | 原图URL |
| albumid | Integer | FOREIGN KEY(album.albumid), NOT NULL | 所属相册ID |
| userid | Integer | FOREIGN KEY(user.userid), NOT NULL | 上传用户ID |

#### 4. 评论表 (comments)
| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| commentid | Integer | PRIMARY KEY, AUTO_INCREMENT | 评论唯一标识 |
| content | String(500) | NOT NULL | 评论内容 |
| create_time | DateTime |  | 创建时间 |
| userid | Integer | FOREIGN KEY(user.userid), NOT NULL | 评论用户ID |
| photoid | Integer | FOREIGN KEY(photos.photoid), NOT NULL | 所属照片ID |
| replyid | Integer | NOT NULL | 回复的评论ID（0表示主评论） |

#### 5. 点赞表 (likes)
| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| likeid | Integer | PRIMARY KEY, AUTO_INCREMENT | 点赞唯一标识 |
| userid | Integer | FOREIGN KEY(user.userid), NOT NULL | 点赞用户ID |
| photoid | Integer | FOREIGN KEY(photos.photoid), NOT NULL | 被赞照片ID |

#### 6. 评论点赞表 (comment_likes)
| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| commentlikeid | Integer | PRIMARY KEY, AUTO_INCREMENT | 评论点赞ID |
| userid | Integer | FOREIGN KEY(user.userid), NOT NULL | 点赞用户ID |
| commentid | Integer | FOREIGN KEY(comments.commentid), NOT NULL | 被赞评论ID |

## 表关系说明

1. **用户表 → 相册表**  
   - 一对多关系 (1:n)
   - 一个用户可以创建多个相册
   - 外键：album.userid → user.userid

2. **用户表 → 照片表**  
   - 一对多关系 (1:n)  
   - 一个用户可以上传多张照片  
   - 外键：photos.userid → user.userid

3. **相册表 → 照片表**  
   - 一对多关系 (1:n)  
   - 一个相册可以包含多张照片  
   - 外键：photos.albumid → album.albumid

4. **用户表 → 评论表**  
   - 一对多关系 (1:n)  
   - 一个用户可以发表多条评论  
   - 外键：comments.userid → user.userid

5. **照片表 → 评论表**  
   - 一对多关系 (1:n)  
   - 一张照片可以有多条评论  
   - 外键：comments.photoid → photos.photoid

6. **用户表 → 点赞表**  
   - 一对多关系 (1:n)  
   - 一个用户可以点赞多张照片  
   - 外键：likes.userid → user.userid

7. **照片表 → 点赞表**  
   - 一对多关系 (1:n)  
   - 一张照片可以被多个用户点赞  
   - 外键：likes.photoid → photos.photoid

8. **用户表 → 评论点赞表**  
   - 一对多关系 (1:n)  
   - 一个用户可以点赞多条评论  
   - 外键：comment_likes.userid → user.userid

9. **评论表 → 评论点赞表**  
   - 一对多关系 (1:n)  
   - 一条评论可以被多个用户点赞  
   - 外键：comment_likes.commentid → comments.commentid

## 非空约束说明

- 所有主键字段均为NOT NULL
- 用户表：username, usertoken, permissions
- 相册表：name, userid
- 照片表：name, albumid, userid
- 评论表：content, userid, photoid, replyid
- 点赞表：userid, photoid
- 评论点赞表：userid, commentid
# ImageGallery
照片墙，前后端分离，使用flask框架编写后端提供接口，前端可接入网页、客户端及各种插件

# 设计思路
一开始是为了自己的mc游戏服务器能快捷分享图片，营造一个更好分享和交流的社区，因此开发了这个项目。这是我自己已经搭建好的基于最新代码的页面 - [萤火相册集](https://image.yanhy.top/)

数据库存储图片链接，分缩略图和原图，客户端浏览器自动缓存缩略图，加快网站访问速度。

当前只能使用api上传，api上传需要带用户信息，确保每个图片都有唯一标识。

为保证不被随意篡改，增加用户权限，`-1`为封禁的用户，·`0`为普通用户，`1`为管理员。

图片展示后可以带图片名称、简介、上传日期，并显示所在相册，如用户上传未指定相册，则相册默认为用户名

可以通过用户名筛选该用户上传的图片，也可以通过相册筛选图片，相册可以任意创建

# 项目架构

- [ImageGallery-Server](./ImageGallery_Server/readme.md)：后端flask服务器，提供api接口，数据库存储图片信息，图片上传、删除、获取等功能
- [ImageGallery-Web](./ImageGallery_Web/readme.md)：前端vue客户端，接入后端api接口，提供图片展示功能
- [ImageGallery-AdminWeb](./ImageGallery_AdminWeb/readme.md)：后台管理系统，提供图片管理、用户管理、相册管理功能
- [ImageGallery-UploadDemo](./ImageGallery_Server/UploadDemo/readme.md)：上传照片实例脚本，可通过指引快速熟悉简单上传图片流程
- [ImageGallery-MCMod](https://github.com/yanhy2000/ImageGallery_MCMod)：mc模组（已分离为独立项目），提供快捷上传截图功能，自动上传到服务器并生成缩略图，提供照片管理、自定义上传等功能

# 开发相关

后端API文档已转移至[开发文档](./ImageGallery_Server/docs/readme.md)
打包编译可参考各个子项目的readme.md

## **Todo**

* 评论系统
* 图片管理客户端
* 消息通知
* 照片排序
* 相册分类

## 开发进展
- [x] 下载图片（Get /api/getphoto）
- [x] 上传图片（Post /api/upload）
- [x] 删除图片（Get /api/delphoto）(图床接入异常，暂时不提供删除图床图片功能)
- [x] 获取图片信息（Get /api/getphotoinfo_all）
- [x] 获取图片公开信息（Get /api/getphotoinfo）
- [x] 获取图片列表（Get /api/photos_list）
- [x] 更新图片信息（PUT /api/updatephoto）
- [x] 获取用户名（Get /api/getusername）
- [x] 新增用户（Post /api/adduser）
- [x] 删除用户（Post /api/deluser）
- [x] 修改用户（Post /api/setuser）
- [x] 不使用图床时切换本地缩略图存储
- [x] 后台Web管理系统
- [x] 后台Web管理接口-图片管理
- [x] 后台Web管理接口-用户管理
- [x] 后台Web管理接口-相册管理
- [x] 创建相册（Post /api/createalbum）
- [x] 更新相册（PUT /api/setalbum）
- [x] 删除相册（DELETE /api/album）
- [x] 用户图片管理
- [x] 点赞like系统
- [ ] 评论系统
- [x] 接入mc模组截图快捷上传
- [x] 网页上传


# 许可证
该项目采用 [GPL-3.0](./LICENSE) 许可证。

# ImageGallery AdminWeb

ImageGallery AdminWeb 是一个基于 Vue.js 的管理后台，用于管理ImageGallery的图片。需配合ImageGallery后端服务使用。

主要编写环境：

- Node.js = 21.7
- Vue.js = 3.5.13
- Vite = 6.0.3
- Axios = 1.7.9

**编译或者运行前，请先将目录下的`copy.env`文件复制为`.env`，并根据实际情况修改`.env`文件中的配置。**

## 目录

- [前提条件](#前提条件)
- [项目安装](#项目安装)
- [开发环境](#开发环境)
- [打包项目](#打包项目)
- [使用示例](#使用示例)
- [许可证](#许可证)

## 前提条件

在运行或打包项目之前，请确保安装了以下软件：

- [Node.js](https://nodejs.org/)（建议使用 21 LTS 版本）

## 项目安装

1. **打开命令行工具**：
   - 在 Windows 上，可以使用命令提示符或 PowerShell。
   - 在 macOS 或 Linux 上，可以使用终端。

2. **导航到项目目录**：
   使用 `cd` 命令进入项目根目录，例如：
   ```bash
   cd /path/to/ImageGallery_AdminWeb
   ```

3. **安装依赖**：
   运行以下命令以安装项目所需的依赖：
   ```bash
   npm install
   ```

## 开发环境

要在本地启动开发服务器以进行开发，您可以使用以下命令：
```bash
npm run dev
```
然后，您可以在浏览器中访问 `http://localhost:5173`来查看应用程序。

## 打包项目

**打包项目前请务必先设置好`.env`文件**
要将项目打包为生产环境文件，您可以运行以下命令：
```bash
npm run build
```
打包完成后，生成的文件将位于 `dist` 目录中，可以将该目录中的文件部署到服务器上。

## 许可证

该项目采用 GPL-3.0 许可证。
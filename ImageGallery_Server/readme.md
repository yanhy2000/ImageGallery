# ImageGallery Server

ImageGallery Server 是一个基于 Flask 的图片墙程序后端，提供图片的存储、转换、上传、下载等接口。

## 目录

- [前提条件](#前提条件)
- [项目安装](#项目安装)
- [部署方式](#部署方式)
- [许可证](#许可证)

## 前提条件

在运行或打包项目之前，请确保安装了以下软件：

- [Python 3.10.10](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)（Python 通常会自动安装）

## 项目安装

1. **打开命令行工具**：
   - 在 Windows 上，可以使用命令提示符或 PowerShell。
   - 在 macOS 或 Linux 上，可以使用终端。

2. **导航到项目目录**：
   使用 `cd` 命令进入项目根目录，例如：
   ```bash
   cd /path/to/ImageGallery_Server
   ```

3. **创建虚拟环境（可选，但推荐）**：
   使用 `venv` 创建一个虚拟环境，以便管理项目依赖：
   ```bash
   python -m venv venv
   ```
   激活虚拟环境：
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **安装依赖**：
   运行以下命令以安装项目所需的依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 部署方式

1. **释放配置文件**：
   进入 `./app` 目录，复制 `config.example.py` 到 `config.py`，并根据实际情况修改配置。

2. **初始化数据库**：
   在项目目录下，运行以下命令以初始化数据库：
   ```bash
   python init_db.py
   ```
3. **运行测试环境服务器**：
   在项目目录下，运行以下命令以启动服务器：
   ```bash
   python run.py
   ```
   服务器默认运行在 `http://localhost:5000`。

4. **运行调试模式**：
   修改 `config.py`，将其中 `DEBUG` 选项设置为 `True`，然后重新启动服务器。

5. **部署生产环境**：
   部署生产环境时，可使用第三方包如Gunicorn。


## 许可证

该项目采用 GPL-3.0 许可证。
# 项目名称

搭配图片墙使用，适用于minecraft fabric客户端。

开发版本：
- Minecraft =1.21.3
- Fabric Loader >=0.16.9


## 目录

- [前提条件](#前提条件)
- [编译步骤](#编译步骤)
- [运行项目](#运行项目)
- [使用示例](#使用示例)
- [许可证](#许可证)

## 前提条件

在编译项目之前，请确保您已安装以下软件：

- [Java JDK](https://www.oracle.com/java/technologies/javase-jdk11-downloads.html)（建议使用版本 11 或更高）
- [Gradle](https://gradle.org/install/)（如果尚未安装，可以选择使用 Gradle Wrapper）

## 编译步骤

1. **打开命令行工具**：
   - 在 Windows 上，可以使用命令提示符或 PowerShell。
   - 在 macOS 或 Linux 上，可以使用终端。

2. **导航到项目目录**：
   使用 `cd` 命令进入包含 `build.gradle` 文件的项目目录，例如：
   ```bash
   cd /path/to/ImageGallery_MCMod
  ```

3. **编译项目**：
   如果您已安装 Gradle，可以直接运行以下命令：
   ```bash
   gradle build
   ```
   如果您希望使用 Gradle Wrapper（推荐），可以使用以下命令：
   ```bash
   ./gradlew build
   ```
   在 Windows 上，您可以使用：
   ```bash
   gradlew.bat build
   ```

4. **查看编译结果**：
   编译成功后，您可以在 `build/libs` 目录下找到生成的 JAR 文件。

## 运行项目

要运行编译后的项目，您可以使用以下命令：
```bash
java -jar build/libs/screenshot_uploader-*.jar
```

## 使用示例

进入游戏后，可在游戏设置内绑定快捷键，使用快捷键进行截图并触发上传按钮。
也可以使用物品“望远镜”，将其使用铁砧重命名为“相机”，右键使用即可进行截图并触发上传按钮。

## 许可证

该项目采用 GPL-3.0 许可证。

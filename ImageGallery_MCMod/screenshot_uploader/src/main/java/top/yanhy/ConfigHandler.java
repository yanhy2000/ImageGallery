package top.yanhy;

import net.fabricmc.loader.api.FabricLoader;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Properties;

public class ConfigHandler {
    private static final String CONFIG_FILE_NAME = "Screenshot_uploader.yml";
    private static final Path CONFIG_PATH = FabricLoader.getInstance().getConfigDir().resolve(CONFIG_FILE_NAME);
    private static Properties properties = new Properties();

    public static void initConfig() {
        try {
            if (!Files.exists(CONFIG_PATH)) {
                // 如果配置文件不存在，则释放默认配置文件
                InputStream defaultConfig = ConfigHandler.class.getResourceAsStream("/" + CONFIG_FILE_NAME);
                if (defaultConfig != null) {
                    Files.copy(defaultConfig, CONFIG_PATH);
                } else {
                    throw new FileNotFoundException("默认配置文件未找到！");
                }
            }
            // 加载配置文件
            try (InputStream input = Files.newInputStream(CONFIG_PATH)) {
                properties.load(input);
            }
        } catch (IOException e) {
            e.printStackTrace();
            throw new RuntimeException("配置文件初始化失败: " + e.getMessage());
        }
    }

    public static String getUsername() {
        return properties.getProperty("username", "player");
    }

    public static String getUserToken() {
        return properties.getProperty("usertoken", "a2d23d45dfg");
    }
}

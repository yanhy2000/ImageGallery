package top.yanhy;

import net.fabricmc.loader.api.FabricLoader;
import net.fabricmc.loader.api.ModContainer;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Objects;
import java.util.Optional;
import java.util.Properties;

import static top.yanhy.Screenshot_uploader.CONFIG_VERSION;


public class ConfigHandler {
    private static final String CONFIG_FILE_NAME = "Screenshot_uploader.yml";
    private static final Path CONFIG_PATH = FabricLoader.getInstance().getConfigDir().resolve(CONFIG_FILE_NAME);
    private static final Properties properties = new Properties();

    public static void initConfig() {
        try {
            if (!Files.exists(CONFIG_PATH)) {
                InputStream defaultConfig = ConfigHandler.class.getResourceAsStream("/" + CONFIG_FILE_NAME);
                if (defaultConfig != null) {
                    Files.copy(defaultConfig, CONFIG_PATH);
                } else {
                    throw new FileNotFoundException("默认配置文件未找到！");
                }
            }
            try (InputStream input = Files.newInputStream(CONFIG_PATH)) {
                properties.load(input);
            }
            // 检查配置文件版本
            String configVersion = properties.getProperty("configversion", "0");
            if(!Objects.equals(configVersion, CONFIG_VERSION)){
                System.out.println("配置文件版本不匹配,旧文件已备份,请手动修改新版配置文件");
                //删除可能存在的旧的bak文件
                Files.delete(CONFIG_PATH.resolveSibling(CONFIG_FILE_NAME + ".bak"));
                //备份当前配置文件
                Files.move(CONFIG_PATH, CONFIG_PATH.resolveSibling(CONFIG_FILE_NAME + ".bak"));
                Files.copy(Objects.requireNonNull(ConfigHandler.class.getResourceAsStream("/" + CONFIG_FILE_NAME)), CONFIG_PATH);
            }
        } catch (IOException e) {
            throw new RuntimeException("配置文件初始化失败: " + e.getMessage());
        }
    }

    public static String getModVersion(String modId) {
        Optional<ModContainer> modContainer = FabricLoader.getInstance().getModContainer(modId);
        return modContainer.map(container -> container.getMetadata().getVersion().getFriendlyString())
                .orElse("unknown");
    }
    public static String getUserToken() {
        return properties.getProperty("usertoken", "token");
    }
    public static String getServerHost() {
        return properties.getProperty("serverhost", "example.com");
    }
    public static int getServerPort() {
        return Integer.parseInt(properties.getProperty("serverport", "8888"));
    }
    public static String getServerHttp() {
        return properties.getProperty("serverhttp", "https");
    }
    public static String getWebUrl() {
        return properties.getProperty("weburl", "");
    }

    public static boolean setUserToken(String userToken) {
        properties.setProperty("usertoken", userToken);
        try (OutputStream output = Files.newOutputStream(CONFIG_PATH)) {
            properties.store(output, "配置文件");
            return true;
        } catch (IOException e) {
            e.printStackTrace();
            return false;
        }
    }

}

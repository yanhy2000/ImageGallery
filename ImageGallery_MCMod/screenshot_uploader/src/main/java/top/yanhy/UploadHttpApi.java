package top.yanhy;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.concurrent.*;

import com.google.gson.Gson;
import net.minecraft.client.MinecraftClient;
import net.minecraft.text.Text;

import static top.yanhy.Screenshot_uploader.MOD_NAME;

public class UploadHttpApi {

    private static final UploadHttpApi INSTANCE = new UploadHttpApi();
    private final ExecutorService executorService = Executors.newSingleThreadExecutor();
    private volatile boolean isUploading = false;

    private UploadHttpApi() {} // 私有构造函数

    public static UploadHttpApi getInstance() {
        return INSTANCE;
    }
    public void uploadImageAsync(String authToken, String imagePath, String imageName, String description, String albumName, String apihost, Integer apiport, String apihttp, UploadCallback callback) {
        if (isUploading) {
            MinecraftClient.getInstance().execute(() -> {
                if (MinecraftClient.getInstance().player != null) {
                    MinecraftClient.getInstance().player.sendMessage(Text.literal(MOD_NAME + "当前正在上传中，请稍后再试。"), false);
                }
            });
            callback.onFailure(new Exception("当前正在上传中，请稍后再试。"));
            return;
        }
        // 提交任务到线程池
        executorService.submit(() -> {
            try {
                isUploading = true;
                UploadResponse response = uploadImage(authToken, imagePath, imageName, description, albumName, apihost, apiport, apihttp);
                callback.onSuccess(response);
            } catch (Exception e) {
                callback.onFailure(e);
            } finally {
                isUploading = false;
            }
        });
    }

    private UploadResponse uploadImage(String authToken, String imagePath, String imageName, String description, String albumName, String apihost, Integer apiport, String apihttp) throws IOException, URISyntaxException {
        String boundary = "Boundary-" + System.currentTimeMillis();
        URL url = new URI(apihttp, null, apihost, apiport, "/api/upload", null, null).toURL();
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();

        connection.setRequestMethod("POST");
        connection.setRequestProperty("Authorization", "Bearer " + authToken);
        connection.setRequestProperty("Content-Type", "multipart/form-data; boundary=" + boundary);

        connection.setDoOutput(true);

        try (
                OutputStream outputStream = connection.getOutputStream();
                PrintWriter writer = new PrintWriter(new OutputStreamWriter(outputStream, StandardCharsets.UTF_8), true)
        ) {
            writer.append("--").append(boundary).append("\r\n");
            writer.append("Content-Disposition: form-data; name=\"file\"; filename=\"").append(imageName).append("\"").append("\r\n");
            writer.append("Content-Type: image/jpeg").append("\r\n");
            writer.append("\r\n").flush();
            File imageFile = new File(imagePath);
            Files.copy(imageFile.toPath(), outputStream);
            outputStream.flush();
            writer.append("\r\n").flush();

            writer.append("--").append(boundary).append("\r\n");
            writer.append("Content-Disposition: form-data; name=\"desc\"").append("\r\n");
            writer.append("\r\n").flush();
            writer.append(description).append("\r\n").flush();

            writer.append("--").append(boundary).append("\r\n");
            writer.append("Content-Disposition: form-data; name=\"album\"").append("\r\n");
            writer.append("\r\n").flush();
            writer.append(albumName).append("\r\n").flush();

            writer.append("--").append(boundary).append("--").append("\r\n").flush();
        } catch (Exception e) {
            System.out.println("在构建请求体时发生错误: " + e.getMessage());
        }

        StringBuilder response = new StringBuilder();
        UploadResponse uploadResponse;
        try {
            int responseCode = connection.getResponseCode();
            if (responseCode == HttpURLConnection.HTTP_OK) {
                try (BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream(), StandardCharsets.UTF_8))) {
                    String line;
                    while ((line = reader.readLine()) != null) {
                        response.append(line.trim());
                    }
                }
                uploadResponse = parseResponse(String.valueOf(response));
            } else {
                System.out.println("请求码错误: " + responseCode + " URL: " + connection.getURL());
                uploadResponse = new UploadResponse();
                uploadResponse.setCode(403);
            }
        } catch (Exception e) {
            System.out.println("在读取响应体时发生错误: " + e.getMessage());
            uploadResponse = new UploadResponse();
            uploadResponse.setCode(500);
        } finally {
            connection.disconnect();
        }
        return uploadResponse;
    }

    public static class UploadResponse {
        private int code;
        private int data;
        private String message;

        // Getters and setters
        public int getCode() { return code; }
        public void setCode(int code) { this.code = code; }

        public int getData() { return data; }
        public void setData(int data) { this.data = data; }

        public String getMessage() { return message; }
        public void setMessage(String message) { this.message = message; }
    }

    public UploadResponse parseResponse(String jsonResponse) {
        Gson gson = new Gson();
        return gson.fromJson(jsonResponse, UploadResponse.class);
    }

    // 回调接口
    public interface UploadCallback {
        void onSuccess(UploadResponse response);
        void onFailure(Exception e);
    }

    public void shutdown() {
        executorService.shutdown();
        try {
            if (!executorService.awaitTermination(5, TimeUnit.SECONDS)) {
                executorService.shutdownNow();
            }
        } catch (InterruptedException e) {
            executorService.shutdownNow();
            Thread.currentThread().interrupt();
        }
    }
}
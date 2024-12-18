package top.yanhy;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import com.google.gson.Gson;

public class UploadHttpApi {

    /**
     * 上传图片到服务器
     *
     * @param authToken   用户鉴权信息
     * @param imagePath   图片路径
     * @param description 图片描述
     * @param albumName   相册名称
     * @return 服务器响应结果
     * @throws IOException 如果发生网络错误
     */
    public UploadResponse uploadImage(String authToken, String imagePath, String description, String albumName, String apiUrl) throws IOException, URISyntaxException {
        String boundary = "Boundary-" + System.currentTimeMillis();
        String url_http = "";
        String url_host = "";
        try {
            url_http = apiUrl.split("://")[0];
            url_host = apiUrl.split("://")[1];
        } catch (Exception e) {
            System.out.println("apiUrl格式错误，请检查:"+apiUrl);
        }
        System.out.println("url_http: " + url_http);
        System.out.println("url_host: " + url_host);
        URL url = new URI(url_http, url_host, "/api/upload", "query").toURL();
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();

        // 设置请求头
        connection.setRequestMethod("POST");
        connection.setRequestProperty("Authorization", "Bearer " + authToken);
        connection.setRequestProperty("Content-Type", "multipart/form-data; boundary=" + boundary);

        // 设置允许写入数据
        connection.setDoOutput(true);

        try (
                OutputStream outputStream = connection.getOutputStream();
                PrintWriter writer = new PrintWriter(new OutputStreamWriter(outputStream, StandardCharsets.UTF_8), true);
        ) {
            // 添加图片文件
            writer.append("--").append(boundary).append("\r\n");
            writer.append("Content-Disposition: form-data; name=\"file\"; filename=\"").append(imagePath).append("\"").append("\r\n");
            writer.append("Content-Type: image/jpeg").append("\r\n");
            writer.append("\r\n").flush();
            Files.copy(Paths.get(imagePath), outputStream);
            outputStream.flush();
            writer.append("\r\n").flush();

            // 添加图片描述
            writer.append("--").append(boundary).append("\r\n");
            writer.append("Content-Disposition: form-data; name=\"desc\"").append("\r\n");
            writer.append("\r\n").flush();
            writer.append(description).append("\r\n").flush();

            // 添加相册名称
            writer.append("--").append(boundary).append("\r\n");
            writer.append("Content-Disposition: form-data; name=\"album\"").append("\r\n");
            writer.append("\r\n").flush();
            writer.append(albumName).append("\r\n").flush();

            // 结束边界
            writer.append("--").append(boundary).append("--").append("\r\n").flush();
        }

        // 获取响应
        StringBuilder response = new StringBuilder();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = reader.readLine()) != null) {
                response.append(line.trim());
            }
        }

        // 关闭连接
        connection.disconnect();

        return parseResponse(response.toString());
    }


    public static class UploadResponse {
        private int code;
        private String message;
        private String data;
        public int getCode() {
            return code;
        }

        public String getMessage() {
            return message;
        }

        public String getData() {
            return data;
        }

        public void setCode(int code) {
            this.code = code;
        }

        public void setMessage(String message) {
            this.message = message;
        }

        public void setData(String data) {
            this.data = data;
        }
    }

    /**
     * 解析服务器返回的JSON响应
     *
     * @param jsonResponse JSON字符串
     * @return 解析后的UploadResponse对象
     */
    public UploadResponse parseResponse(String jsonResponse) {
        Gson gson = new Gson();
        return gson.fromJson(jsonResponse, UploadResponse.class);
    }
}

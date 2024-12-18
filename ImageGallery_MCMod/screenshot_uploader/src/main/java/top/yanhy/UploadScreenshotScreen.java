package top.yanhy;

import net.minecraft.client.MinecraftClient;
import net.minecraft.client.gui.DrawContext;
import net.minecraft.client.gui.screen.Screen;
import net.minecraft.client.gui.widget.ButtonWidget;
import net.minecraft.client.gui.widget.TextFieldWidget;
import net.minecraft.client.toast.SystemToast;
import net.minecraft.text.Text;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import static top.yanhy.Screenshot_uploader.USERNAME;

public class UploadScreenshotScreen extends Screen {
    private static final Logger LOGGER = LogManager.getLogger("ScreenshotUploader");
    private final String filename;
    private TextFieldWidget descriptionField;
    private TextFieldWidget albumField;

    public UploadScreenshotScreen(String filename) {
        super(Text.literal("上传图片到图片墙"));
        this.filename = filename;
    }

    @Override
    protected void init() {
        this.descriptionField = new TextFieldWidget(this.textRenderer, this.width / 2 - 100, this.height / 2 - 50, 200, 20, Text.literal("图片描述"));
        this.descriptionField.setSuggestion("这个人很懒，什么都没写");
        this.descriptionField.setMaxLength(50);
        this.addSelectableChild(this.descriptionField);
        this.descriptionField.setFocusUnlocked(true);
        this.descriptionField.setChangedListener(text -> {
            this.descriptionField.setSuggestion(null);
        });

        this.albumField = new TextFieldWidget(this.textRenderer, this.width / 2 - 100, this.height / 2 - 20, 200, 20, Text.literal("相册集"));
        this.albumField.setSuggestion("留空默认使用用户名");
        this.albumField.setMaxLength(15);
        this.addSelectableChild(this.albumField);
        this.albumField.setFocusUnlocked(true);
        this.albumField.setChangedListener(text -> {
            this.albumField.setSuggestion(null);
        });

        ButtonWidget buttonUpload = ButtonWidget.builder(Text.of("上传"), (btn) -> {
            if (this.client != null) {
                handleUpload(this.filename, this.descriptionField.getText(), this.albumField.getText());
                this.client.getToastManager().add(
                        SystemToast.create(this.client, SystemToast.Type.NARRATOR_TOGGLE, Text.of("上传中..."), Text.of("开始上传图片墙"))
                );
            }
        }).dimensions(this.width / 2 - 110, this.height / 2 + 20, 100, 20).build();

        ButtonWidget buttonClose = ButtonWidget.builder(Text.of("取消"), (btn) -> {
            if (this.client != null) {
                //关闭当前窗口
                close();
            }
        }).dimensions(this.width / 2 + 10, this.height / 2 + 20, 100, 20).build();
        this.addDrawableChild(buttonUpload);
        this.addDrawableChild(buttonClose);
    }
    @Override
    public void render(DrawContext context, int mouseX, int mouseY, float delta) {
        super.render(context, mouseX, mouseY, delta);

//        this.renderBackground(context);
        this.renderBackground(context,mouseX,mouseY,delta);
        context.drawText(this.textRenderer, this.title, this.width / 2-40, this.height / 2 - 80, 0xFFFFFFFF, true);
        super.render(context, mouseX, mouseY, delta);
        this.descriptionField.render(context, mouseX, mouseY, delta);
        this.albumField.render(context, mouseX, mouseY, delta);

    }

    private void handleUpload(String filename, String description, String album) {
        if (album.isEmpty()) {
            album = USERNAME;
        }
        if (description.isEmpty()) {
            description = "这个人很懒，什么都没写";
        }
        LOGGER.info("上传截图: 文件名={}, 描述={}, 相册={}", filename, description, album);
        if (MinecraftClient.getInstance().player != null) {
            MinecraftClient.getInstance().player.sendMessage(Text.literal("上传测试成功！"), false);
        }
        this.close();
    }

    @Override
    public void close() {
        MinecraftClient.getInstance().setScreen(null);
    }
}

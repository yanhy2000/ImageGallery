package top.yanhy;

import net.minecraft.client.MinecraftClient;
import net.minecraft.client.gui.DrawContext;
import net.minecraft.client.gui.screen.Screen;
import net.minecraft.client.gui.widget.ButtonWidget;
import net.minecraft.client.gui.widget.TextFieldWidget;
import net.minecraft.text.Text;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.IOException;
import java.net.URISyntaxException;

import static top.yanhy.Screenshot_uploader.*;


public class EditConfigScreen extends Screen {
    private static final Logger LOGGER = LogManager.getLogger("ScreenshotUploader");
    private TextFieldWidget userTokenField;

    public EditConfigScreen() {
        super(Text.literal("图片墙Token配置"));
    }

    @Override
    protected void init() {
        this.userTokenField = new TextFieldWidget(this.textRenderer, this.width / 2 - 100, this.height / 2 - 50, 200, 20, Text.literal("用户Token"));
        this.userTokenField.setSuggestion("aaaaa-bbbbb-ccccc-ddddd");
        this.userTokenField.setMaxLength(100);
        this.addSelectableChild(this.userTokenField);
        this.userTokenField.setFocusUnlocked(true);
        this.userTokenField.setChangedListener(_ -> this.userTokenField.setSuggestion(null));

        ButtonWidget buttonConfirm = ButtonWidget.builder(Text.of("确认"), (_) -> {
            if (this.client != null) {
                try {
                    handleConfirm(this.userTokenField.getText());
                } catch (IOException | URISyntaxException e) {
                    throw new RuntimeException(e);
                }
            }
        }).dimensions(this.width / 2 - 110, this.height / 2 + 20, 100, 20).build();

        ButtonWidget buttonClose = ButtonWidget.builder(Text.of("取消"), (_) -> {
            if (this.client != null) {
                close();
            }
        }).dimensions(this.width / 2 + 10, this.height / 2 + 20, 100, 20).build();
        this.addDrawableChild(buttonConfirm);
        this.addDrawableChild(buttonClose);
    }
    @Override
    public void render(DrawContext context, int mouseX, int mouseY, float delta) {
        super.render(context, mouseX, mouseY, delta);
        this.renderBackground(context,mouseX,mouseY,delta);
        context.drawText(this.textRenderer, this.title, this.width / 2-40, this.height / 2 - 80, 0xFFFFFFFF, true);
        super.render(context, mouseX, mouseY, delta);
        this.userTokenField.render(context, mouseX, mouseY, delta);
    }

    private void handleConfirm(String userToken) throws IOException, URISyntaxException {
        if (userToken.isEmpty()) {
            LOGGER.error("用户Token为空, 请填写用户Token!");
            if (MinecraftClient.getInstance().player != null) {
                MinecraftClient.getInstance().player.sendMessage(Text.literal("用户Token为空, 请填写用户Token!"), false);
            }
            return;
        }
        boolean storetoken = ConfigHandler.setUserToken(userToken);
        if (storetoken) {
            LOGGER.info("用户Token保存成功!");
            if (MinecraftClient.getInstance().player != null) {
                MinecraftClient.getInstance().player.sendMessage(Text.literal("用户Token保存成功!"), false);
            }
            reloadConfig();
        } else {
            LOGGER.error("用户Token保存失败!");
            if (MinecraftClient.getInstance().player != null) {
                MinecraftClient.getInstance().player.sendMessage(Text.literal("用户Token保存失败!"), false);
            }
        }
        this.close();
    }

    @Override
    public void close() {
        MinecraftClient.getInstance().setScreen(null);
    }
}

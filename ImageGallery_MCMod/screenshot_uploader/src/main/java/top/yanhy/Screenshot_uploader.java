package top.yanhy;

import com.mojang.brigadier.Command;
import com.mojang.brigadier.builder.LiteralArgumentBuilder;
import com.mojang.brigadier.arguments.StringArgumentType;
import com.mojang.brigadier.builder.RequiredArgumentBuilder;
import com.mojang.brigadier.context.CommandContext;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.command.v2.ClientCommandRegistrationCallback;
import net.fabricmc.fabric.api.client.command.v2.FabricClientCommandSource;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.client.keybinding.v1.KeyBindingHelper;
import net.fabricmc.fabric.api.command.v2.CommandRegistrationCallback;
import net.fabricmc.fabric.api.event.player.UseItemCallback;
import net.minecraft.client.MinecraftClient;
import net.minecraft.client.option.KeyBinding;
import net.minecraft.client.util.InputUtil;
import net.minecraft.client.util.ScreenshotRecorder;
import net.minecraft.item.ItemStack;
import net.minecraft.item.Items;
import net.minecraft.server.command.CommandManager;
import net.minecraft.server.command.ServerCommandSource;
import net.minecraft.text.ClickEvent;
import net.minecraft.text.HoverEvent;
import net.minecraft.text.Style;
import net.minecraft.text.Text;
import net.minecraft.util.ActionResult;


import org.lwjgl.glfw.GLFW;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Optional;

public class Screenshot_uploader implements ClientModInitializer {
	public static final String MOD_ID = "screenshot_uploader";
	public static final String MOD_NAME = "[相机]";
	public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);
	public static List<String> file_info = new ArrayList<>();
	public static String file_path = "";

	public static final String VERSION = ConfigHandler.getModVersion(MOD_ID);
	public static String USERTOKEN = "";
	public static String SERVERHOST = "";
	public static Integer SERVERPORT = 0;
	public static String SERVERHTTP = "";


	@Override
	public void onInitializeClient() {
        LOGGER.info("Screenshot_uploader mod initialized! version: {}", VERSION);
		ConfigHandler.initConfig();
		USERTOKEN = ConfigHandler.getUserToken();
		SERVERHOST = ConfigHandler.getServerHost();
		SERVERPORT = ConfigHandler.getServerPort();
		SERVERHTTP = ConfigHandler.getServerHttp();
		LOGGER.info("加载配置文件成功");

		KeyBinding screenshotKey = KeyBindingHelper.registerKeyBinding(new KeyBinding("截图上传快捷键", InputUtil.Type.KEYSYM, GLFW.GLFW_KEY_P, "key.category.screenshot_uploader"));
		ClientTickEvents.END_CLIENT_TICK.register(client -> {
			if (screenshotKey.wasPressed()) {
				screenshot();
			}
		});
		LOGGER.info("注册快捷键成功");

		registerClientCommands();
		LOGGER.info("客户端命令注册成功");

		UseItemCallback.EVENT.register((player, world, hand) -> {
			ItemStack itemStack = player.getStackInHand(hand);
			if (itemStack.getItem() == Items.SPYGLASS && itemStack.getName().getString().contains("相机")) {
				if (world.isClient) {
					if (Objects.equals(USERTOKEN, "token" ) || Objects.equals(SERVERHOST, "example.com")){
						File mcDirectory = MinecraftClient.getInstance().runDirectory;
						File configFile = new File(mcDirectory, "config/screenshot_uploader.yml");
						if (MinecraftClient.getInstance().player != null) {
							Text configButton = Text.literal("[打开配置文件]")
									.setStyle(Style.EMPTY
											.withColor(0x00FF00)
											.withClickEvent(new ClickEvent(ClickEvent.Action.OPEN_FILE, configFile.getAbsolutePath()))
											.withHoverEvent(new HoverEvent(HoverEvent.Action.SHOW_TEXT, Text.literal("点击打开配置文件。")))
									);
							Text message = Text.literal(MOD_NAME + "请先在配置文件中配置用户名和用户Token，保存后请重启游戏。" )
									.append(configButton);
							MinecraftClient.getInstance().player.sendMessage(message, false);
						}
						return ActionResult.FAIL;
					}

					screenshot();

					return ActionResult.FAIL;
				}
				return ActionResult.FAIL;
			}

			return ActionResult.PASS;
		});
		LOGGER.info("注册物品成功");
	}
	public void registerClientCommands() {
		ClientCommandRegistrationCallback.EVENT.register((dispatcher, registryAccess) -> {
			dispatcher.register(
					LiteralArgumentBuilder.<FabricClientCommandSource>literal("uploadScreenshot")
							.then(RequiredArgumentBuilder.<FabricClientCommandSource, String>argument("filename", StringArgumentType.string())
									.executes(context -> executeUploadCommandwithargs(context.getSource(), StringArgumentType.getString(context, "filename"))))
							.executes(context -> executeUploadCommand(context.getSource()))
			);
		});
	}

	private void screenshot() {
		try {
			LOGGER.info("开始截图...");
			ScreenshotRecorder.saveScreenshot(
					MinecraftClient.getInstance().runDirectory,
					MinecraftClient.getInstance().getFramebuffer(),
					(file)->{
						file.visit((string) -> {
							file_info.add(string);
							return Optional.empty();
						});
						file_path = file_info.get(1);
						if (MinecraftClient.getInstance().player != null) {
							MinecraftClient.getInstance().player.sendMessage(file, false);
							Text uploadButton = Text.literal("[上传到图片墙]")
									.setStyle(Style.EMPTY
											.withColor(0x00FF00)
											.withClickEvent(new ClickEvent(ClickEvent.Action.RUN_COMMAND, "/uploadScreenshot " + file_path))
											.withHoverEvent(new HoverEvent(HoverEvent.Action.SHOW_TEXT, Text.literal("点击上传截图到图片墙。命令: /uploadScreenshot " + file_path)))
									);
							Text message = Text.literal(MOD_NAME + "截图已保存。" )
									.append(uploadButton);
							MinecraftClient.getInstance().player.sendMessage(message, false);
							file_info.clear();
						}
					}
			);
		} catch (Exception e) {
			LOGGER.error("快捷键截图失败: {}", e.getMessage());
			if (MinecraftClient.getInstance().player != null) {
				MinecraftClient.getInstance().player.sendMessage(Text.literal("快捷键截图失败，请查看日志。"), false);
			}
		}
	}

	private int executeUploadCommandwithargs(FabricClientCommandSource source,String  filename) {
		source.sendFeedback(Text.of("执行上传截图命令，文件名：" + filename));
		MinecraftClient client = MinecraftClient.getInstance();
		if (client.player != null) {
			client.execute(() -> client.setScreen(new UploadScreenshotScreen(filename)));
		}
		return Command.SINGLE_SUCCESS;
	}

	public int executeUploadCommand(FabricClientCommandSource source) {
		source.sendFeedback(Text.of("执行缺少参数的命令"));
        if (MinecraftClient.getInstance().player != null) {
            MinecraftClient.getInstance().player.sendMessage(Text.literal(MOD_NAME + "需要指定参数，请使用 /uploadScreenshot filename"), false);
        }
        return Command.SINGLE_SUCCESS;
	}

}

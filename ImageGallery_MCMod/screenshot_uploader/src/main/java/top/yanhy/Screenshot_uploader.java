package top.yanhy;

import com.mojang.brigadier.Command;
import com.mojang.brigadier.builder.LiteralArgumentBuilder;
import com.mojang.brigadier.arguments.StringArgumentType;
import com.mojang.brigadier.context.CommandContext;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.command.v2.CommandRegistrationCallback;
import net.fabricmc.fabric.api.event.player.UseItemCallback;
import net.minecraft.client.MinecraftClient;
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

	public static final String VERSION = "1.0.0";
	public static String USERNAME = "";
	public static String USERTOKEN = "";
	public static String SERVERHOST = "";
	public static Integer SERVERPORT = 0;
	public static String SERVERHTTP = "";


	@Override
	public void onInitializeClient() {
		LOGGER.info("Screenshot_uploader mod initialized! version: " + VERSION);
		ConfigHandler.initConfig();
		USERNAME = ConfigHandler.getUsername();
		USERTOKEN = ConfigHandler.getUserToken();
		SERVERHOST = ConfigHandler.getServerHost();
		SERVERPORT = ConfigHandler.getServerPort();
		SERVERHTTP = ConfigHandler.getServerHttp();
		LOGGER.info("加载配置文件成功");
		CommandRegistrationCallback.EVENT.register((dispatcher, dedicated,environment) -> {
			dispatcher.register(
					LiteralArgumentBuilder.<ServerCommandSource>literal("uploadScreenshot")
							.then(CommandManager.argument("filename", StringArgumentType.string())
									.executes(this::executeUploadCommandwithargs))
							.executes(this::executeUploadCommand)
			);
		});
		UseItemCallback.EVENT.register((player, world, hand) -> {
			ItemStack itemStack = player.getStackInHand(hand);

			if (itemStack.getItem() == Items.SPYGLASS && itemStack.getName().getString().contains("相机")) {
				if (world.isClient) {
					if (Objects.equals(USERNAME, "username") || Objects.equals(USERTOKEN, "token")){
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
					try {
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
						LOGGER.error("截图失败: {}", e.getMessage());
						player.sendMessage(Text.literal("截图失败，请查看日志。"), false);
					}

					return ActionResult.FAIL;
				}
				return ActionResult.FAIL;
			}

			return ActionResult.PASS;
		});
	}

	private int executeUploadCommandwithargs(CommandContext<ServerCommandSource> context) {
		String filename = context.getArgument("filename", String.class);
		LOGGER.info("上传截图命令触发，文件名: {}", filename);
		MinecraftClient client = MinecraftClient.getInstance();
		if (client.player != null) {
			client.execute(() -> client.setScreen(new UploadScreenshotScreen(filename)));
		}
		return Command.SINGLE_SUCCESS;
	}

	public int executeUploadCommand(CommandContext<ServerCommandSource> context) {
        if (MinecraftClient.getInstance().player != null) {
            MinecraftClient.getInstance().player.sendMessage(Text.literal(MOD_NAME + "需要指定参数，请使用 /uploadScreenshot filename"), false);
        }
        return Command.SINGLE_SUCCESS;
	}

}

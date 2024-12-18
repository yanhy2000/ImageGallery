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

	@Override
	public void onInitializeClient() {
		LOGGER.info("Screenshot_uploader mod initialized! version: " + VERSION);
		// 初始化配置文件
		ConfigHandler.initConfig();
		USERNAME = ConfigHandler.getUsername();
		USERTOKEN = ConfigHandler.getUserToken();

		LOGGER.info("加载配置文件成功 - Username: {}, UserToken: {}", USERNAME, USERTOKEN);
		// 注册命令
		CommandRegistrationCallback.EVENT.register((dispatcher, dedicated,environment) -> {
			dispatcher.register(
					LiteralArgumentBuilder.<ServerCommandSource>literal("uploadScreenshot")
							.then(CommandManager.argument("filename", StringArgumentType.string())
									.executes(this::executeUploadCommandwithargs))  // 有文件名参数
							.executes(this::executeUploadCommand)  // 没有文件名参数
			);
		});
		// 注册监听玩家使用物品事件
		UseItemCallback.EVENT.register((player, world, hand) -> {
			ItemStack itemStack = player.getStackInHand(hand);

			if (itemStack.getItem() == Items.SPYGLASS && itemStack.getName().getString().contains("相机")) {
				if (world.isClient) {
					if (Objects.equals(USERNAME, "username") || Objects.equals(USERTOKEN, "token")){
						player.sendMessage(Text.literal(MOD_NAME + "请先在配置文件中配置用户名和用户Token。"), false);
						return ActionResult.FAIL;
					}
					try {
						ScreenshotRecorder.saveScreenshot(
								MinecraftClient.getInstance().runDirectory, // 保存路径
								MinecraftClient.getInstance().getFramebuffer(), // 当前帧缓冲区
								(file)->{
									file.visit((string) -> {
										file_info.add(string);
                                        return Optional.empty();
                                    });
									file_path = file_info.get(1);

									// 发送消息给玩家
                                    if (MinecraftClient.getInstance().player != null) {
                                        MinecraftClient.getInstance().player.sendMessage(file, false);
										// 构建 "上传" 按钮
										Text uploadButton = Text.literal("[上传到图片墙]")
												.setStyle(Style.EMPTY
														.withColor(0x00FF00) // 设置绿色
														.withClickEvent(new ClickEvent(ClickEvent.Action.RUN_COMMAND, "/uploadScreenshot " + file_path)) // 点击时执行的命令
														.withHoverEvent(new HoverEvent(HoverEvent.Action.SHOW_TEXT, Text.literal("点击上传截图到图片墙。命令: /uploadScreenshot " + file_path))) // 鼠标悬停时显示命令内容
												);
										// 构建完整消息
										Text message = Text.literal(MOD_NAME + "截图已保存。" )
												.append(uploadButton);

										// 发送消息到聊天框
										MinecraftClient.getInstance().player.sendMessage(message, false);
										file_info.clear();
                                    }
                                }
						);
					} catch (Exception e) {
						LOGGER.error("截图失败: {}", e.getMessage());
						player.sendMessage(Text.literal("截图失败，请查看日志。"), false);
					}

					return ActionResult.FAIL; // 拦截使用事件
				}
				return ActionResult.FAIL; // 拦截使用事件
			}

			return ActionResult.PASS; // 其他物品正常使用
		});
	}

	// 处理上传截图的命令
	private int executeUploadCommandwithargs(CommandContext<ServerCommandSource> context) {
		String filename = context.getArgument("filename", String.class);
		// 在日志中输出文件名
		LOGGER.info("上传截图命令触发，文件名: {}", filename);

		// 你可以在这里调用截图上传逻辑，例如上传到图床
//        if (MinecraftClient.getInstance().player != null) {
//            MinecraftClient.getInstance().player.sendMessage(Text.literal(MOD_NAME + "正在上传截图: " + filename), false);
//        }
		// 打开上传界面
		MinecraftClient client = MinecraftClient.getInstance();
		if (client.player != null) {
			client.execute(() -> client.setScreen(new UploadScreenshotScreen(filename)));
		}

        // 你可以在这里编写具体的上传逻辑，例如将文件上传到远程服务器
		return Command.SINGLE_SUCCESS;
	}

	public int executeUploadCommand(CommandContext<ServerCommandSource> context) {
        if (MinecraftClient.getInstance().player != null) {
            MinecraftClient.getInstance().player.sendMessage(Text.literal(MOD_NAME + "需要指定参数，请使用 /uploadScreenshot filename"), false);
        }
        return Command.SINGLE_SUCCESS;
	}

}

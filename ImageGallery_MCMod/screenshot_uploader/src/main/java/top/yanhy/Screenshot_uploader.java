package top.yanhy;

import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.event.player.UseItemCallback;
import net.minecraft.client.MinecraftClient;
import net.minecraft.client.util.ScreenshotRecorder;
import net.minecraft.item.ItemStack;
import net.minecraft.item.Items;
import net.minecraft.text.Text;
import net.minecraft.util.ActionResult;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Screenshot_uploader implements ClientModInitializer {
	public static final String MOD_ID = "screenshot_uploader";
	public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

	@Override
	public void onInitializeClient() {
		LOGGER.info("Screenshot_uploader mod initialized!");

		// 注册监听玩家使用物品事件
		UseItemCallback.EVENT.register((player, world, hand) -> {
			ItemStack itemStack = player.getStackInHand(hand);

			// 判断物品是否为望远镜并且重命名为“相机”
			if (itemStack.getItem() == Items.SPYGLASS && itemStack.getName().getString().contains("相机")) {
				if (world.isClient) { // 确保在客户端执行
					LOGGER.info("玩家 {} 使用了被命名为 '相机' 的望远镜，正在截图...", player.getName().getString());

					// 执行截图
					try {
						ScreenshotRecorder.saveScreenshot(
								MinecraftClient.getInstance().runDirectory, // 保存路径
								MinecraftClient.getInstance().getFramebuffer(), // 当前帧缓冲区
								(filename)->{LOGGER.info("截图已保存到文件: {}", filename);}
						);
						player.sendMessage(Text.literal("截图已保存到游戏截图文件夹。"), false);
						LOGGER.info("截图保存成功！");
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
}

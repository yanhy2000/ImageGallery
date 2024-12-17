package top.yanhy;

import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.event.player.UseItemCallback;
import net.minecraft.item.ItemStack;
import net.minecraft.item.Items;


import net.minecraft.util.ActionResult;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Screenshot_uploader implements ModInitializer {
	public static final String MOD_ID = "screenshot_uploader";
	public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

	@Override
	public void onInitialize() {
		LOGGER.info("mod initialized!");

		// 注册监听玩家使用物品事件
		UseItemCallback.EVENT.register((player, world, hand) -> {
			ItemStack itemStack = player.getStackInHand(hand);
			// 判断物品是否为望远镜并重命名为相机
			if (itemStack.getItem() == Items.SPYGLASS && itemStack.getName().getString().contains("相机")) {
				LOGGER.info("玩家 {} 使用了望远镜-相机，已拦截。", player.getName().getString());
				return ActionResult.FAIL;
			}
			LOGGER.info("玩家 {} 在世界 {} 使用了物品 {}。", player.getName().getString(), world.getRegistryKey().getValue().toString(),itemStack.getName().getString());

			return ActionResult.PASS;
		});
	}
}

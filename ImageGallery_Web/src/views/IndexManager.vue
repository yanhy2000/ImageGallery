<template>
    <div class="container">
        <header class="header">
            <h1>{{ title }}</h1>
            <h2>{{ subtitle }}</h2>
            <button class="login-button" @click="showLoginModal">登录</button>
            <button class="mode-toggle-btn" @click="toggleDarkMode">
                <i :class="DarkMode ? 'fa-solid fa-sun' : 'fa-solid fa-moon'"></i> </button>
        </header>

        <div class="UserGuide" @mouseenter="showTooltip" @mouseleave="hideTooltip" @click="toggleTooltip">
            <h3>网站使用说明</h3>
            <div v-show="isTooltipVisible" class="tooltip">
                网站使用说明：
                <br> 点击图片可放大查看，点击右上角按钮切换黑白模式。
                <br> 鼠标悬停在图片上可查看图片信息。
                <br> 点击刷新缓存按钮可清除浏览器缓存，并重新加载页面。
                <br> 点击每页展示数量下拉框可调整每页展示数量。
                <br> 网站会占用浏览器缓存以提高访问速度，缓存过期时间为7天。如缓存过大可手动清理浏览器缓存。
                <br>
                <br> 上传图片：
                <br> 目前不支持直接网页上传，需配合MC模组截图上传，模组可在群文件下载“[图片墙辅助]screenshot_uploader-1.0.0”。
                <br> 每个人有一个专属token，在模组加载后修改配置文件时需要提供，申请token可联系yanhy2000。
                <br> 上传图片后，暂无修改、删除入口，可找管理员后台修改。
            </div>
        </div>

        <main class="image-gallery" :style="gridStyle">
            <div v-for="photo in photos" :key="photo.photoid" class="image-card" :style="imageCardStyle"
                @click="getPhotoInfo(photo.photoid)">
                <img :src="photo.thumbnailUrl" :alt="photo.desc" loading="lazy">
                <div class="overlay">
                    <div class="overlay-content">
                        <p>{{ photo.upload_user }}</p>
                        <p>{{ photo.upload_time }}</p>
                        <p>{{ photo.desc }}</p>
                    </div>
                </div>
                <!-- 放大按钮 -->
                <div class="expand-button" @click.stop="openModal(photo)">
                    <i class="fa-solid fa-expand"></i>
                </div>
                <!-- 点赞区域 -->
                <div class="like-section" @click.stop="toggleLike(photo.photoid)">
                    <i class="fa-regular fa-heart" :class="{ 'fa-solid': photo.isLiked, 'liked': photo.isLiked }"></i>
                    <span class="like-count">{{ photo.likes }}</span>
                </div>
            </div>
        </main>

        <div class="pagination">
            <button @click="changePage('first')" :disabled="currentPage <= 1" title="首页">
                <i class="fa-solid fa-angles-left"></i>
            </button>
            <button @click="changePage('prev')" :disabled="currentPage <= 1" title="上一页">
                <i class="fa-solid fa-angle-left"></i>
            </button>
            <span class="page-info">第 {{ currentPage }} 页 / 共 {{ totalPages }} 页</span>
            <button @click="changePage('next')" :disabled="currentPage >= totalPages" title="下一页">
                <i class="fa-solid fa-angle-right"></i>
            </button>
            <button @click="changePage('last')" :disabled="currentPage >= totalPages" title="尾页">
                <i class="fa-solid fa-angles-right"></i>
            </button>
        </div>

        <div class="per-page-selector">
            <label for="perPageSelect">每页展示数量：</label>
            <div class="custom-select-wrapper">
                <select id="perPageSelect" v-model="perPage" @change="fetchPhotos" class="custom-select">
                    <option v-for="option in perPageOptions" :key="option" :value="option">{{ option }}</option>
                </select>
            </div>
            <div><button class="refresh-cache-button" @click="refreshCache">刷新缓存</button></div>
        </div>

        <transition name="fade">
            <div v-if="imageModalVisible" class="image-modal" @click="imageModalClick">
                <div class="modal-content" @click.stop>
                    <img :src="currentThumbnailUrl ? currentThumbnailUrl : ''"
                        :alt="currentImage ? currentImage.desc : ''" class="modal-image">
                    <div class="image-info">
                        <p>{{ currentImage.desc }}</p>
                        <p>
                            <span>图片ID：{{ currentImage.photoid }}</span>
                            <span>上传时间：{{ currentImage.upload_time }}</span>
                            <span>上传者：{{ currentImage.uploader }}</span>
                            <span>相册：{{ currentImage.albumname }}</span>
                        </p>
                    </div>
                    <button @click="closeImageModal" class="close-button" title="关闭">
                        <i class="fa-solid fa-xmark"></i>
                    </button>
                </div>
            </div>
        </transition>

        <transition name="fade">
            <div v-if="LoginModalVisible" class="login-modal" @click="loginModalClick">
                <div class="modal-content" @click.stop>
                    <p>请登录</p>
                    <button @click="closeLoginModal" class="close-button" title="关闭">
                        <i class="fa-solid fa-xmark"></i>
                    </button>
                </div>
            </div>
        </transition>
        <br>
        <br>
        <footer class="custom-footer">
            <div class="footer-content">
                <p>Powered by <a href="https://github.com/yanhy2000/ImageGallery" target="_blank">ImageGallery</a></p>
                <p>{{ displayContent }}</p>
                <p>Copyright © <span id="footer-year"></span> yanhy2000</p>
            </div>
        </footer>
    </div>
</template>

<script>
import { ref, onMounted, computed, onBeforeUnmount } from 'vue';
import { usePhotoManager, useModalManager, useDarkMode, useTooltip } from '@/composables';
import { refreshCache, cleanExpiredPhotos } from '@/services/cacheService';

export default {
    name: 'IndexManager',
    setup() {
        const title = import.meta.env.VITE_APP_TITLE;
        const subtitle = import.meta.env.VITE_APP_SUBTITLE;
        const perPageOptions = [6, 9, 15, 20, 25, 30];
        const year = new Date().getFullYear();

        const {
            photos,
            currentPage,
            totalPages,
            perPage,
            totalPhotos,
            error,
            fetchPhotos,
            getPhotoInfo,
        } = usePhotoManager();

        const {
            imageModalVisible,
            LoginModalVisible,
            currentImage,
            currentThumbnailUrl,
            closeImageModal,
            showLoginModal,
            closeLoginModal,
            loginModalClick,
            imageModalClick,
        } = useModalManager();

        const { DarkMode, toggleDarkMode } = useDarkMode();

        const { isTooltipVisible, showTooltip, hideTooltip, toggleTooltip } = useTooltip();

        const config = ref({
            version: '1.0.2',
            customContent: import.meta.env.VITE_APP_CUSTOM_CONTENT,
        });

        const displayContent = computed(() => {
            return config.value.customContent
                ? `${config.value.customContent} V${config.value.version}`
                : `${title}  V${config.value.version}`;
        });

        const changePage = (action) => {
            if (action === 'first') {
                currentPage.value = 1;
            } else if (action === 'prev' && currentPage.value > 1) {
                currentPage.value--;
            } else if (action === 'next' && currentPage.value < totalPages.value) {
                currentPage.value++;
            } else if (action === 'last') {
                currentPage.value = totalPages.value;
            }
            fetchPhotos();
        };

        const toggleLike = (photoid) => {

            const photo = photos.value.find((photo) => photo.photoid === photoid);
            if (photo) {
                photo.isLiked = !photo.isLiked; // 切换点赞状态
                photo.likes += photo.isLiked ? 1 : -1; // 点赞数增减
            }

            // const photo = photos.value.find((photo) => photo.photoid === photoid);
            // if (photo) {
            //     photo.isLiked = !photo.isLiked;
            //     fetchPhotos();
            // }
        };
        const imageCardStyle = computed(() => {
            const { imageSizeScale } = calculateGrid(perPage.value);

            return {
                transform: `scale(${imageSizeScale})`,
            };
        });

        const gridStyle = computed(() => {
            const { columns, gap } = calculateGrid(perPage.value);

            return {
                gridTemplateColumns: `repeat(${columns}, 1fr)`,
                gap,
            };
        });

        const calculateGrid = (numberOfPhotos) => {
            const isMobile = window.innerWidth <= 768;

            let columns = isMobile ? 2 : Math.min(5, Math.ceil(Math.sqrt(numberOfPhotos)));
            let rows = Math.ceil(numberOfPhotos / columns);

            let imageSizeScale = isMobile ? 1.1 : 1;
            let gap = '80px';

            if (!isMobile) {
                if (numberOfPhotos <= 6) {
                    imageSizeScale = 1.2;
                    gap = '80px';
                } else if (numberOfPhotos > 6 && numberOfPhotos <= 15) {
                    imageSizeScale = 1;
                    gap = '40px';
                } else if (numberOfPhotos > 15) {
                    imageSizeScale = 0.9;
                    gap = '30px';
                }
            } else {
                if (numberOfPhotos <= 6) {
                    imageSizeScale = 1;
                    gap = '30px';
                } else if (numberOfPhotos > 6 && numberOfPhotos <= 15) {
                    imageSizeScale = 1;
                    gap = '20px';
                } else if (numberOfPhotos > 15) {
                    imageSizeScale = 0.9;
                    gap = '10px';
                }
            }

            return { columns, rows, imageSizeScale, gap };
        };

        const handleEscKey = (event) => {
            if (event.key === 'Escape' && imageModalVisible.value) {
                imageModalVisible.value = false;
            }
        };

        const checkDarkMode = () => {
            const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)');
            if (prefersDarkMode.matches) {
                DarkMode.value = true;
                document.body.classList.add('dark-mode');
            } else {
                DarkMode.value = false;
                document.body.classList.remove('dark-mode');
            }
            prefersDarkMode.addEventListener('change', () => { });
        }

        onMounted(async () => {
            const isMobile = window.innerWidth <= 768;
            if (isMobile) {
                perPage.value = 6;
            }
            checkDarkMode();
            await fetchPhotos();
            await cleanExpiredPhotos();
            await fetchPhotos();
            const link = document.createElement('link');
            link.rel = 'icon';
            link.href = 'img/favicon.ico';
            document.head.appendChild(link);
            document.addEventListener('keydown', handleEscKey);
            document.getElementById("footer-year").innerText = year;
        });

        onBeforeUnmount(() => {
            document.removeEventListener('keydown', handleEscKey);
        });

        return {
            title,
            subtitle,
            photos,
            currentPage,
            totalPages,
            perPage,
            perPageOptions,
            currentImage,
            currentThumbnailUrl,
            imageModalVisible,
            totalPhotos,
            error,
            changePage,
            fetchPhotos,
            getPhotoInfo,
            closeImageModal,
            closeLoginModal,
            LoginModalVisible,
            loginModalClick,
            showLoginModal,
            toggleDarkMode,
            DarkMode,
            imageModalClick,
            imageCardStyle,
            gridStyle,
            refreshCache,
            displayContent,
            isTooltipVisible,
            hideTooltip,
            showTooltip,
            toggleTooltip,
            toggleLike,
        };
    },
};
</script>

<style>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
@import '@/css/index.css';
@import '@/css/image-modal.css';
@import '@/css/login-modal.css';
@import '@/css/pagination.css';
@import '@/css/btn.css';
@import '@/css/like.css';
@import '@/css/expand.css';
</style>
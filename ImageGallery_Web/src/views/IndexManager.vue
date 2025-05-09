<template>
    <div class="container">
        <Header />

        <div class="UserGuide" @mouseenter="showTooltip" @mouseleave="hideTooltip" @click="toggleTooltip">
            <h3>网站说明</h3>
            <div v-show="isTooltipVisible" class="tooltip" v-html="custom_text"></div>
        </div>

        <main class="image-gallery" :style="gridStyle">
            <div v-for="photo in photos" :key="photo.photoid" class="image-card" :style="imageCardStyle"
                @click="getPhotoInfo(photo.photoid)">
                <img :src="photo.thumbnailUrl" :alt="photo.desc" loading="lazy" />
                <div class="overlay">
                    <div class="overlay-content">
                        <p>{{ photo.upload_user }}</p>
                        <p>{{ photo.upload_time }}</p>
                        <p>{{ photo.desc }}</p>
                    </div>
                </div>
                <!-- 点赞部分 -->
                <div class="action-section">
                    <div class="like-section" @click.stop="toggleLike(photo.photoid)">
                        <i class="fa-regular fa-heart" :class="{ 'fa-solid': photo.isLiked, liked: photo.isLiked }"></i>
                        <span class="like-count">{{ photo.likes }}</span>
                    </div>
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
                    <option v-for="option in perPageOptions" :key="option" :value="option">
                        {{ option }}
                    </option>
                </select>
            </div>
            <div>
                <button class="refresh-cache-button" @click="refreshCache">
                    刷新缓存
                </button>
            </div>
        </div>

        <transition name="fade">
            <div v-if="imageModalVisible" class="image-modal" @click="imageModalClick">
                <div class="image-modal-content" @click.stop>
                    <img :src="currentThumbnailUrl ? currentThumbnailUrl : ''"
                        :alt="currentImage ? currentImage.desc : ''" class="modal-image" />
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

        

        <Foot />
    </div>
</template>

<script>
import { ref, onMounted, computed, onBeforeUnmount } from "vue";
import axios from "axios";

import {
    cachePhoto,
    getCachedPhoto,
    cleanExpiredPhotos,
    refreshCache,
} from "@/services/cacheService";
import Header from '@/components/Header.vue'
import Foot from '@/components/Foot.vue'

export default {
    name: "IndexManager",
    components: { Header, Foot },
    setup() {

        const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
        const custom_text = import.meta.env.VITE_APP_CUSTOM_CONTENT.replace(
            /\n/g,
            "<br>"
        );
        const photos = ref([]);
        const currentPage = ref(1);
        const totalPages = ref(1);
        const perPage = ref(6);
        const currentImage = ref(null);
        const currentThumbnailUrl = ref(null);
        const imageModalVisible = ref(false);

        const CommentModalVisible = ref(false);
        const totalPhotos = ref(0);
        const perPageOptions = [6, 9, 15, 20, 25, 30];
        const error = ref(null);
        const isTooltipVisible = ref(false);


        const changePage = (action) => {
            if (action === "first") {
                currentPage.value = 1;
            } else if (action === "prev" && currentPage.value > 1) {
                currentPage.value--;
            } else if (action === "next" && currentPage.value < totalPages.value) {
                currentPage.value++;
            } else if (action === "last") {
                currentPage.value = totalPages.value;
            }
            fetchPhotos();
            checkUserLikes();
        };

        // 点赞功能
        const toggleLike = async (photoid) => {
            const photo = photos.value.find((photo) => photo.photoid === photoid);
            if (!photo) return;

            try {
                const storedToken = localStorage.getItem("jwttoken");
                if (!storedToken) {
                    alert("请先登录");
                    return;
                }
                const endpoint = photo.isLiked ? "/api/unlikephoto" : "/api/likephoto";
                const response = await axios.post(
                    `${import.meta.env.VITE_API_BASE_URL}${endpoint}`,
                    { photoid },
                    {
                        headers: {
                            Authorization: `Bearer ${storedToken}`,
                        },
                    }
                );

                if (response.data.code === 200) {
                    photo.isLiked = !photo.isLiked;
                    photo.likes += photo.isLiked ? 1 : -1;
                } else {
                    alert("操作失败，请稍后重试");
                }
            } catch (error) {
                console.error("点赞操作失败", error);
                alert("点赞操作失败，请稍后重试");
            }
        };

        const checkUserLikes = async () => {
            const storedToken = localStorage.getItem("jwttoken");
            if (!storedToken) return;

            try {
                const response = await axios.get(
                    `${import.meta.env.VITE_API_BASE_URL}/api/userlikes`,
                    {
                        headers: {
                            Authorization: `Bearer ${storedToken}`,
                        },
                        params: {
                            page: 1,
                            perpage: 999
                        }
                    }
                );

                if (response.data.code === 200) {
                    const likes = response.data.data.likes;
                    for (let i = 0; i < likes.length; i++) {
                        const photoid = likes[i].photoid;
                        const photo = photos.value.find(
                            (photo) => photo.photoid === photoid
                        );
                        if (photo) {
                            photo.isLiked = true;
                        }
                    }
                }
            } catch (error) {
                console.error("checkUserLikes获取用户点赞状态失败", error);
            }
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

            let columns = isMobile
                ? 2
                : Math.min(5, Math.ceil(Math.sqrt(numberOfPhotos)));
            let rows = Math.ceil(numberOfPhotos / columns);

            let imageSizeScale = isMobile ? 1.1 : 1;
            let gap = "80px";

            if (!isMobile) {
                if (numberOfPhotos <= 6) {
                    imageSizeScale = 1.2;
                    gap = "80px";
                } else if (numberOfPhotos > 6 && numberOfPhotos <= 15) {
                    imageSizeScale = 1;
                    gap = "40px";
                } else if (numberOfPhotos > 15) {
                    imageSizeScale = 0.9;
                    gap = "30px";
                }
            } else {
                if (numberOfPhotos <= 6) {
                    imageSizeScale = 1;
                    gap = "30px";
                } else if (numberOfPhotos > 6 && numberOfPhotos <= 15) {
                    imageSizeScale = 1;
                    gap = "20px";
                } else if (numberOfPhotos > 15) {
                    imageSizeScale = 0.9;
                    gap = "10px";
                }
            }

            return { columns, rows, imageSizeScale, gap };
        };

        const fetchPhotos = async () => {
            try {
                const response = await axios.get(
                    `${import.meta.env.VITE_API_BASE_URL}/api/photos_list?page=${currentPage.value
                    }&perpage=${perPage.value}`
                );

                if (response.status !== 200) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = response.data;

                if (data.code == 200) {
                    photos.value = data.data.photos;
                    totalPhotos.value = data.data.totalPhotos;
                    totalPages.value = data.data.totalPages;

                    for (let i = 0; i < photos.value.length; i++) {
                        const photo = photos.value[i];

                        const likeResponse = await axios.get(
                            `${import.meta.env.VITE_API_BASE_URL}/api/getphotolikecount`,
                            { params: { photoid: photo.photoid } }
                        );

                        if (likeResponse.data.code === 200) {
                            photos.value[i].likes = likeResponse.data.data.likes || 0;
                        } else {
                            photos.value[i].likes = 0;
                        }

                        const thumbnailUrl = await fetchThumbnail(photo.photoid);
                        if (thumbnailUrl) {
                            photos.value[i].thumbnailUrl = thumbnailUrl;
                        }
                    }
                } else {
                    error.value = data.message;
                }
            } catch (e) {
                console.error("Failed to fetch photos:", e);
                if (e.status == 401) {
                    alert("Token unauthorized!");
                }
                error.value = e.message;
            } finally{
                await checkUserLikes();
            }
        };

        const fetchThumbnail = async (photoId) => {
            try {
                const cachedPhoto = await getCachedPhoto(photoId);

                if (cachedPhoto) {
                    console.log(`Using cached thumbnail for photo ${photoId}`);

                    if (cachedPhoto.blob) {
                        return URL.createObjectURL(cachedPhoto.blob);
                    }

                    return cachedPhoto.thumbnailUrl;
                }

                console.log(`Fetching thumbnail for photo ${photoId} from network...`);
                const response = await fetch(
                    `${import.meta.env.VITE_API_BASE_URL}/api/getphoto?photoid=${photoId}`
                );
                if (response.ok) {
                    const thumbnailBlob = await response.blob();
                    const thumbnailUrl = URL.createObjectURL(thumbnailBlob);

                    await cachePhoto(photoId, thumbnailUrl, thumbnailBlob);

                    return thumbnailUrl;
                } else {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
            } catch (e) {
                console.error(`Failed to fetch thumbnail for photo ${photoId}:`, e);
                return "";
            }
        };

        const getPhotoInfo = async (photoid) => {
            try {
                const response = await axios.get(
                    `${import.meta.env.VITE_API_BASE_URL
                    }/api/getphotoinfo?photoid=${photoid}`
                );
                if (response.data.code === 200) {
                    currentImage.value = response.data.data;

                    const likeResponse = await axios.get(
                        `${import.meta.env.VITE_API_BASE_URL}/api/getphotolikecount`,
                        { params: { photoid } }
                    );

                    if (likeResponse.data.code === 200) {
                        currentImage.value.likes = likeResponse.data.data.likes || 0;
                    } else {
                        currentImage.value.likes = 0;
                    }

                    currentThumbnailUrl.value = await fetchThumbnail(photoid);
                    imageModalVisible.value = true;
                } else {
                    alert("Failed to load photo info");
                }
            } catch (error) {
                console.error("Error fetching photo info:", error);
            }
        };

        const closeImageModal = () => {
            imageModalVisible.value = false;
            currentImage.value = null;
            currentThumbnailUrl.value = null;
        };

        const handleEscKey = (event) => {
            if (
                event.key === "Escape" &&
                (imageModalVisible.value ||
                    CommentModalVisible.value)
            ) {
                imageModalVisible.value = false;
                CommentModalVisible.value = false;
            }
        };

        const imageModalClick = (event) => {
            if (event.target === event.currentTarget) {
                imageModalVisible.value = false;
            }
        };

        const showTooltip = () => {
            isTooltipVisible.value = true;
        };

        const hideTooltip = () => {
            isTooltipVisible.value = false;
        };

        const toggleTooltip = () => {
            isTooltipVisible.value = !isTooltipVisible.value;
        };

        

        onMounted(async () => {
            const isMobile = window.innerWidth <= 768;
            if (isMobile) {
                perPage.value = 6;
            }
            await fetchPhotos();
            
            await cleanExpiredPhotos();
            const link = document.createElement("link");
            link.rel = "icon";
            link.href = "img/favicon.ico";

            document.head.appendChild(link);
            document.addEventListener("keydown", handleEscKey);
        });

        onBeforeUnmount(() => {
            document.removeEventListener("keydown", handleEscKey);
        });

        return {
            API_BASE_URL,
            custom_text,
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

            imageModalClick,
            imageCardStyle,
            gridStyle,
            refreshCache,
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
@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css");
@import "@/css/index.css";
@import "@/css/image-modal.css";
@import "@/css/utils-modal.css";
@import "@/css/btn.css";
@import "@/css/action.css";
@import "@/css/status-bar.css";
@import "@/css/account-page.css";
@import "@/css/upload-page.css";
</style>

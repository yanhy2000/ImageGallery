<template>
    <div class="container">
        <header class="header">
            <h1>{{ title }}</h1>
            <h2>{{ subtitle }}</h2>
            <button class="mode-toggle-btn" @click="toggleDarkMode">
                <i :class="DarkMode ? 'fa-solid fa-sun' : 'fa-solid fa-moon'"></i> </button>
        </header>

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
            <div v-if="imageModalVisible" class="image-modal" @click="handleModalBackgroundClick">
                <div class="modal-content" @click.stop>
                    <img :src="currentThumbnailUrl ? currentThumbnailUrl : ''"
                        :alt="currentImage ? currentImage.desc : ''" class="modal-image">
                    <div class="image-info">
                        <p>{{ currentImage.desc }}</p>
                        <p>
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
import axios from 'axios';
import { cachePhoto, getCachedPhoto, cleanExpiredPhotos, refreshCache } from '@/services/cacheService';

export default {
    name: 'IndexManager',
    setup() {
        const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
        const title = import.meta.env.VITE_APP_TITLE;
        const subtitle = import.meta.env.VITE_APP_SUBTITLE;
        const photos = ref([]);
        const currentPage = ref(1);
        const totalPages = ref(1);
        const perPage = ref(9);
        const currentImage = ref(null);
        const currentThumbnailUrl = ref(null);
        const imageModalVisible = ref(false);
        const totalPhotos = ref(0);
        const perPageOptions = [6, 9, 15, 20, 25, 30];
        const error = ref(null);
        const DarkMode = ref(false);
        const config = ref({
            version: '1.0.1',
            customContent: import.meta.env.VITE_APP_CUSTOM_CONTENT,
        });
        const year = new Date().getFullYear();
        
        const displayContent = computed(() => {
            return config.value.customContent
                ? `${config.value.customContent} V${config.value.version}`
                : `${title.value}  V${config.value.version}`;
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
            let columns = Math.min(5, Math.ceil(Math.sqrt(numberOfPhotos)));
            let rows = Math.ceil(numberOfPhotos / columns);

            let imageSizeScale = 1;
            let gap = '80px';

            if (numberOfPhotos <= 6) {
                imageSizeScale = 1.2;
                gap = '80px';
            } else if (numberOfPhotos > 6 && numberOfPhotos <= 15) {
                imageSizeScale = 1;
                gap = '40px';
            }
            else if (numberOfPhotos > 15 && numberOfPhotos <= 30) {
                imageSizeScale = 0.9;
                gap = '30px';
            }
            else if (numberOfPhotos > 30) {
                imageSizeScale = 0.8;
                gap = '10px';
            }

            return { columns, rows, imageSizeScale, gap };
        };

        const fetchPhotos = async () => {
            try {
                const response = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/api/photos_list?page=${currentPage.value}&perpage=${perPage.value}`);

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
                        const thumbnailUrl = await fetchThumbnail(photo.photoid);
                        if (thumbnailUrl) {
                            photos.value[i] = { ...photo, thumbnailUrl };
                        }
                    }
                }
                else {
                    error.value = data.message;
                }
            } catch (e) {
                console.error('Failed to fetch photos:', e);
                if (e.status == 401) {
                    alert('Token unauthorized!');
                }
                error.value = e.message;
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
                const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/getphoto?photoid=${photoId}`);
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
                return '';
            }
        };


        const getPhotoInfo = async (photoid) => {
            try {
                const response = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/api/getphotoinfo?photoid=${photoid}`);
                if (response.data.code === 200) {
                    currentImage.value = response.data.data;
                    currentThumbnailUrl.value = await fetchThumbnail(photoid);
                    imageModalVisible.value = true;
                } else {
                    alert('Failed to load photo info');
                }
            } catch (error) {
                console.error('Error fetching photo info:', error);
            }
        };

        const closeImageModal = () => {
            imageModalVisible.value = false;
            currentImage.value = null;
            currentThumbnailUrl.value = null;
        };

        const openImageModal = () => {
            imageModalVisible.value = true;
        };

        const handleEscKey = (event) => {
            if (event.key === 'Escape' && imageModalVisible.value) {
                imageModalVisible.value = false;
            }
        };

        const handleModalBackgroundClick = (event) => {
            if (event.target === event.currentTarget) {
                imageModalVisible.value = false;
            }
        };

        const toggleDarkMode = () => {
            DarkMode.value = !DarkMode.value;
            if (DarkMode.value) {
                document.body.classList.add('dark-mode');
            } else {
                document.body.classList.remove('dark-mode');
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
            await fetchPhotos();
            checkDarkMode();
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
            prefersDarkMode.removeEventListener('change', listener);
        });

        return {
            API_BASE_URL,
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
            openImageModal,
            toggleDarkMode,
            DarkMode,
            handleModalBackgroundClick,
            imageCardStyle,
            gridStyle,
            refreshCache,
            displayContent,
        };
    },
};
</script>

<style>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
@import '@/css/index.css';
@import '@/css/modal.css';
@import '@/css/pagination.css';
@import '@/css/btn.css';
</style>
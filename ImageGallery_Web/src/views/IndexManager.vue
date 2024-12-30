<template>
    <div class="container">
        <header class="header">
            <h1>{{ title }}</h1>
            <h2>{{ subtitle }}</h2>
            <button class="mode-toggle-btn" @click="toggleDarkMode">
                <i :class="DarkMode ? 'fa-solid fa-sun' : 'fa-solid fa-moon'"></i> </button>
        </header>

        <main class="image-gallery">
            <div v-for="photo in photos" :key="photo.photoid" class="image-card" @click="getPhotoInfo(photo.photoid)">
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
            <select id="perPageSelect" v-model="perPage" @change="fetchImages">
                <option v-for="option in perPageOptions" :key="option" :value="option">{{ option }}</option>
            </select>
        </div>

        <div v-if="imageModalVisible" class="image-modal" @click="handleModalBackgroundClick">
            <div class="modal-content" @click.stop>
                <img :src="currentThumbnailUrl ? currentThumbnailUrl : ''" :alt="currentImage ? currentImage.desc : ''"
                    class="modal-image">
                <div class="image-info">
                    <p>描述：{{ currentImage.desc }}</p>
                    <p>上传时间：{{ currentImage.upload_time }}</p>
                    <p>上传者：{{ currentImage.uploader }}</p>
                    <p>相册：{{ currentImage.albumname }}</p>
                </div>
                <button @click="closeImageModal" class="close-button" title="关闭">
                    <i class="fa-solid fa-xmark"></i>
                </button>
            </div>
        </div>

    </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import axios from 'axios';

export default {
    name: 'IndexManager',
    setup() {
        const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
        const title = import.meta.env.VITE_APP_TITLE;
        const subtitle = import.meta.env.VITE_APP_SUBTITLE;
        const photos = ref([]);
        const currentPage = ref(1);
        const totalPages = ref(1);
        const perPage = ref(10);
        const currentImage = ref(null);
        const currentThumbnailUrl = ref(null);
        const imageModalVisible = ref(false);
        const totalPhotos = ref(0);
        const perPageOptions = [10, 20, 30, 40, 50];
        const error = ref(null);
        const DarkMode = ref(false);


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
                    await fetchAllThumbnails();
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
        const fetchThumbnail = async (photoid) => {
            try {
                const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/getphoto?photoid=${photoid}`);
                if (response.ok) {
                    return URL.createObjectURL(await response.blob());
                } else {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
            } catch (e) {
                console.error('Failed to fetch thumbnail:', e);
                return '';
            }
        }

        const fetchAllThumbnails = async () => {
            for (let i = 0; i < photos.value.length; i++) {
                const photo = photos.value[i];
                const thumbnailUrl = await fetchThumbnail(photo.photoid);
                if (thumbnailUrl) {
                    photos.value[i] = { ...photo, thumbnailUrl };
                }
            }
        };

        const getPhotoInfo = async (photoid) => {
            try {
                const response = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/api/getphotoinfo?photoid=${photoid}`);
                if (response.data.code === 200) {
                    currentImage.value = response.data.data;
                    currentThumbnailUrl.value = await fetchThumbnail(photoid);
                    console.log(currentThumbnailUrl.value);
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
            prefersDarkMode.addEventListener('change', () => {});
        }

        onMounted(() => {
            fetchPhotos();
            checkDarkMode();
            const link = document.createElement('link');
            link.rel = 'icon';
            link.href = 'img/favicon.ico';
            document.head.appendChild(link);
            document.addEventListener('keydown', handleEscKey);


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
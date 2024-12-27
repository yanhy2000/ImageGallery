<template>
    <div class="container">
        <header class="header">
            <h1>{{ title }}</h1>
            <h2>{{ subtitle }}</h2>
            <!-- 白天/夜间模式按钮 -->
            <button class="mode-toggle-btn" @click="toggleMode">🌙</button>
        </header>

        <!-- 图片展示区域 -->
        <div class="image-gallery">
            <div v-for="photo in photos" :key="photo.photoid" class="image-card" @click="getPhotoInfo(photo.photoid)">
                <img :src="photo.thumbnailUrl" :alt="photo.desc">
                <div class="overlay">
                    <div class="overlay-content">
                        <p>{{ photo.upload_user }}</p>
                        <p>{{ photo.upload_time }}</p>
                        <p>{{ photo.desc }}</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="pagination">
            <button @click="changePage('first')" :disabled="currentPage <= 1">首页</button>
            <button @click="changePage('prev')" :disabled="currentPage <= 1">上一页</button>
            <span>第 {{ currentPage }} 页，共 {{ totalPages }} 页</span>
            <button @click="changePage('next')" :disabled="currentPage >= totalPages">下一页</button>
            <button @click="changePage('last')" :disabled="currentPage >= totalPages">尾页</button>
        </div>
        <div class="per-page-selector">
            <label for="perPageSelect">每页展示数量：</label>
            <select id="perPageSelect" v-model="perPage" @change="fetchImages">
                <option v-for="option in perPageOptions" :key="option" :value="option">{{ option }}</option>
            </select>
        </div>

        <!-- 图片查看模态框 -->
        <div v-if="imageModalVisible" class="image-modal" @click="toggleImageSize">
            <div class="modal-content">
                <img :src="currentImage ? currentImage.thumbnailUrl : ''" alt="Current Image" class="modal-image">
                <div class="image-info">
                    <p>描述：{{ currentImage ? currentImage.desc : '' }}</p>
                    <p>上传时间：{{ currentImage ? currentImage.upload_time : '' }}</p>
                    <p>上传者：{{ currentImage ? currentImage.uploader : '' }}</p>
                    <p>相册: {{ currentImage ? currentImage.albumname : '' }}</p>
                </div>
            </div>
        </div>

    </div>
</template>

<script>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
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
        const currentIndex = ref(0);
        const imageModalVisible = ref(false);
        const hoveredPhotoId = ref(null);
        const isNightMode = ref(false);
        const totalPhotos = ref(0);
        const perPageOptions = [10, 20, 30, 40, 50];
        const error = ref(null);


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

        // 获取单张图片信息
        const getPhotoInfo = async (photoid) => {
            hoveredPhotoId.value = photoid;
            console.log(hoveredPhotoId.value);
            try {
                const response = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/api/getphotoinfo?photoid=${photoid}`);
                if (response.data.code === 200) {
                    currentImage.value = response.data.data;
                    const thumbnailUrl = await fetchThumbnail(photoid);
                    if (thumbnailUrl) {
                        currentImage.value= { ...currentImage, thumbnailUrl };
                    }
                    imageModalVisible.value = true;
                } else {
                    alert('Failed to load photo info');
                }
            } catch (error) {
                console.error('Error fetching photo info:', error);
            }
        };

        const closeModal = () => {
            imageModalVisible.value = false;
            hoveredPhotoId.value = null;
            currentImage.value = null;
            // document.querySelector('.modal-image').classList.remove('zoomed');
        };

        const toggleImageSize = () => {
            imageModalVisible.value = !imageModalVisible.value;
        };

        // 切换白天/夜间模式
        const toggleMode = () => {
            isNightMode.value = !isNightMode.value;
            if (isNightMode.value) {
                document.body.classList.add('night-mode');
            } else {
                document.body.classList.remove('night-mode');
            }
        };

        onMounted(() => {
            fetchPhotos();
            const link = document.createElement('link');
            link.rel = 'icon';
            link.href = 'img/favicon.ico';
            document.head.appendChild(link);
        });

        onBeforeUnmount(() => {
            // 清理逻辑
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
            currentIndex,
            imageModalVisible,
            hoveredPhotoId,
            isNightMode,
            totalPhotos,
            error,
            changePage,
            fetchPhotos,
            getPhotoInfo,
            closeModal,
            toggleImageSize,
            toggleMode,
        };
    },
};
</script>

<style>
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f5f5f5;
    color: #33333373;
    transition: background-color 0.3s ease, color 0.3s ease;
}

body.night-mode {
    background-color: #2c2c2c;
    color: #96fff6;
    transition: background-color 0.3s ease, color 0.3s ease;
}

.header {
    text-align: center;
    margin-bottom: 30px;
}

body.night-mode .header h1 {
    color: #ddd !important;
}

body.night-mode .header h2 {
    color: #fff !important;
}

.mode-toggle-btn {
    position: absolute;
    top: 20px;
    right: 20px;
    padding: 10px 10px;
    background-color: #2fe4eb81;
    color: white;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    font-size: 18px;
    transition: background-color 0.3s;
}

.mode-toggle-btn:hover {
    background-color: #3e86f157;
}

body::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('img/background.png') no-repeat center center/cover;
    z-index: -1;
    filter: blur(8px);
}

.container {
    max-width: 1200px;
    margin: 20px auto;
    padding: 10px;
}

.header {
    text-align: center;
    margin-bottom: 30px;
}

.header h1 {
    font-size: 36px;
    color: #333;
}

.header h2 {
    font-size: 18px;
    color: #555;
}

.image-gallery {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
}

.image-card {
    position: relative;
    cursor: pointer;
    transition: transform 0.3s ease;
}

.image-card:hover {
    transform: scale(1.05);
}

.image-card img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 8px;
    transition: transform 0.3s ease;
}

.image-card .overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    opacity: 0;
    transition: opacity 0.3s ease;
    border-radius: 8px;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
}

.image-card .overlay-content {
    text-align: center;
    padding: 10px;
}

.image-card:hover .overlay {
    opacity: 1;
}

button {
    background-color: #ff6600;
    border: none;
    color: white;
    padding: 8px 16px;
    cursor: pointer;
    border-radius: 4px;
    font-size: 14px;
    transition: background-color 0.3s ease;
    transform: scale(1);
}

button:hover {
    background-color: #e65c00;
}

.image-modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.7);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 999;
    backdrop-filter: blur(5px);
}

.modal-content {
    background-color: #fff;
    padding: 20px;
    border-radius: 8px;
    max-width: 90%;
    max-height: 80%;
    overflow-y: auto;
}

.modal-image {
    max-width: 100%;
    height: auto;
    transition: transform 0.3s ease;
}

.image-info {
    margin-top: 20px;
    text-align: center;
}

/* 分页按钮 */
.pagination {
    text-align: center;
}
/* 每页展示数量 */
.per-page-selector {
    text-align: center;
}
</style>
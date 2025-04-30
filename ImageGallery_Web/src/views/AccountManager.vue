<template>
    <div class="container">
        <Header />
        <div class="back-home-container">
            <button class="back-home" @click="handleBackToHome">
                <i class="fa-solid fa-house"></i> 返回主页
            </button>
        </div>

        <main class="account-management">
            <!-- 标签页切换 -->
            <div class="tab-container">
                <button class="tab-button" :class="{ 'active': activeTab === 'photos' }" @click="switchTab('photos')">
                    图片管理
                </button>
                <button class="tab-button" :class="{ 'active': activeTab === 'albums' }" @click="switchTab('albums')">
                    相册管理
                </button>
            </div>

            <!-- 图片管理 -->
            <div v-if="activeTab === 'photos'" class="management-content">
                <div class="table-container">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>图片ID</th>
                                <th>预览</th>
                                <th>描述</th>
                                <th>相册名</th>
                                <th>上传时间</th>
                                <th>操作</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="photo in photoList" :key="photo.photoid">
                                <td>{{ photo.photoid }}</td>
                                <td>
                                    <img :src="photo.thumbnailUrl" class="thumbnail-img">
                                </td>
                                <td>{{ photo.desc || '无描述' }}</td>
                                <td>{{ photo.album_name }}</td>
                                <td>{{ formatDateTime(photo.upload_time) }}</td>
                                <td>
                                    <button class="action-button delete-button" @click="deletePhoto(photo.photoid)">
                                        删除
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>

                    <!-- 分页控制 -->
                    <div class="pagination-controls">
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
                            <select id="perPageSelect" v-model="perPage" @change="fetchPhoto">
                                <option v-for="option in perPageOptions" :key="option" :value="option">
                                    {{ option }}
                                </option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 相册管理 -->
            <div v-if="activeTab === 'albums'" class="management-content">
                <div class="table-container">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>相册ID</th>
                                <th>相册名称</th>
                                <th>创建时间</th>
                                <th>操作</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="album in albumList" :key="album.albumid">
                                <td>{{ album.albumid }}</td>
                                <td>{{ album.name }}</td>
                                <td>{{ formatDateTime(album.create_time) }}</td>
                                <td>
                                    <button class="action-button delete-button" @click="deleteAlbum(album.albumid)">
                                        删除
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>

                    <!-- 分页控制 -->
                    <div class="pagination-controls">
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
                            <select id="perPageSelect" v-model="perPage" @change="fetchPhoto">
                                <option v-for="option in perPageOptions" :key="option" :value="option">
                                    {{ option }}
                                </option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>
        </main>

        <transition name="fade">
            <div v-if="StatusModalVisible" class="login-modal">
                <div class="modal-content">
                    <h2>{{ statusTitle }}</h2>
                    <button @click="closeModal" class="close-button" title="关闭">
                        <i class="fa-solid fa-xmark"></i>
                    </button>
                    <div class="input-group">
                        <p class="success">{{ statusContent }}</p>
                    </div>
                </div>
            </div>
        </transition>

        <Foot />
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import Header from '@/components/Header.vue'
import Foot from '@/components/Foot.vue'
import { useRouter } from 'vue-router';
import {
    cachePhoto,
    getCachedPhoto,
    cleanExpiredPhotos,
    refreshCache,
} from "@/services/cacheService";
export default {
    components: { Header, Foot },
    setup() {
        const router = useRouter();
        const activeTab = ref('photos');
        const photoList = ref([]);
        const albumList = ref([]);
        const currentPage = ref(1);
        const totalPages = ref(1);
        const perPage = ref(10);
        const perPageOptions = [5, 10, 15, 20, 25, 30];
        const storedToken = ref("");
        const handleBackToHome = () => router.push('/');

        const StatusModalVisible = ref(false);
        const statusTitle = ref("Title");
        const statusContent = ref("Content");

        const switchTab = (tab) => {
            activeTab.value = tab;
            currentPage.value = 1;
            fetchPhoto();
        };

        const formatDateTime = (datetime) => {
            if (!datetime) return '';
            return new Date(datetime).toLocaleString();
        };

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
            fetchPhoto();
        };

        const openModal = () => {
            StatusModalVisible.value = true;
        }
        const closeModal = () => {
            StatusModalVisible.value = false;
        }

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

        const fetchPhoto = async () => {

            try {
                const config = {
                    headers: {
                        Authorization: `Bearer ${storedToken.value}`
                    },
                    params: {
                        page: currentPage.value,
                        perpage: perPage.value
                    }
                };

                if (activeTab.value === 'photos') {
                    const response = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/api/user_photos`, config);
                    if (response.status !== 200) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    const data = response.data;
                    if (data.code == 200) {
                        photoList.value = response.data.data.photos;
                        totalPages.value = response.data.data.totalPages;
                        for (let i = 0; i < photoList.value.length; i++) {
                            const photo = photoList.value[i];

                            const likeResponse = await axios.get(
                                `${import.meta.env.VITE_API_BASE_URL}/api/getphotolikecount`,
                                { params: { photoid: photo.photoid } }
                            );

                            if (likeResponse.data.code === 200) {
                                photoList.value[i].likes = likeResponse.data.data.likes || 0;
                            } else {
                                photoList.value[i].likes = 0;
                            }

                            const thumbnailUrl = await fetchThumbnail(photo.photoid);
                            if (thumbnailUrl) {
                                photoList.value[i].thumbnailUrl = thumbnailUrl;
                            }
                        }
                    } else {
                        error.value = data.message;
                    }
                } else {
                    const response = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/api/user_albums`, config);
                    albumList.value = response.data.data.albums;
                    totalPages.value = response.data.data.totalPages;
                }
            } catch (error) {
                console.error('获取数据失败:', error);
            }
        };
        // 获取相册
        const fetchAlbums = async () => {
            try {
                const config = {
                    headers: {
                        Authorization: `Bearer ${storedToken.value}`
                    },
                    params: {
                        page: currentPage.value,
                        perpage: perPage.value
                    }
                };

                const response = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/api/user_albums`, config);
                if (response.status !== 200) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = response.data;
                if (data.code === 200) {
                    albums.value = data.data.albums;
                    totalAlbums.value = data.data.totalAlbums;
                    totalPages.value = data.data.totalPages;
                } else {
                    error.value = data.message;
                }
            } catch (e) {
                error.value = e.message;
            }
        };
        //实现删除逻辑
        const deletePhoto = async (photoid) => {
            try {
                const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/api/del_user_photo`, {
                    photoid: photoid
                }, {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${storedToken.value}`
                    }
                });

                if (response.status !== 200) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = response.data;

                if (data.code === 200) {
                    alert("succ")
                } else {
                    alert(data);
                }
            } catch (e) {
                alert(e.message);
            } finally {
                closeModal();
            }
        };
        //删除相册
        const deleteAlbum = async (albumid) => {
            try {
                const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/api/del_user_album`, {
                    albumid: albumid
                }, {
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${storedToken.value}`
                    }
                });

                if (response.status !== 200) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = response.data;

                if (data.code === 200) {
                    alert("succ")
                } else {
                    alert(data);
                }
            } catch (e) {
                alert(e.message);
            } finally {
                closeModal();
            }
        };

        onMounted(() => {
            storedToken.value = localStorage.getItem("jwttoken");
            if (!storedToken.value) {
                throw new Error("请先登录");
            }
            fetchPhoto();
            fetchAlbums();
        });

        return {
            handleBackToHome,
            activeTab,
            photoList,
            albumList,
            currentPage,
            totalPages,
            perPage,
            perPageOptions,
            switchTab,
            changePage,
            formatDateTime,
            deletePhoto,
            deleteAlbum
        };
    }
};
</script>

<style scoped></style>
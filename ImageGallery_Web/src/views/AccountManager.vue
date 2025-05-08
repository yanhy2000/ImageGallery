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
                                    <button class="action-button delete-button" @click="openDeletePhotoModal(photo.photoid)">
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
                            <select id="perPageSelect" v-model="perPage" @change="fetchAll">
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
                                    <button class="action-button delete-button" @click="openDeleteAlbumModal(album.albumid)">
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
                            <select id="perPageSelect" v-model="perPage" @change="fetchAll">
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
            <div v-if="deletePhotoModalVisible" class="modal-overlay">
                <div class="modal-content modal-content--medium">
                    <h2 class="modal-title">删除图片</h2>
                    <button @click="closeDeletePhotoModal" class="modal-close-button" title="关闭">
                        <i class="fa-solid fa-xmark"></i>
                    </button>
                    <div class="modal-content-group">
                        <p class="modal-message modal-message--error">确定要删除ID为{{SelectPhotoid}}的图片吗？</p>
                        <div class="modal-button-group">
                            <button class="modal-button modal-button--cancel" @click="closeDeletePhotoModal">取消</button>
                            <button class="modal-button modal-button--danger" @click="confirmDeletePhoto">确认删除</button>
                        </div>
                    </div>
                </div>
            </div>
        </transition>

        <transition name="fade">
            <div v-if="deleteAlbumModalVisible" class="modal-overlay">
                <div class="modal-content modal-content--medium">
                    <h2 class="modal-title">删除相册</h2>
                    <button @click="closeDeleteAlbumModal" class="close-button" title="关闭">
                        <i class="fa-solid fa-xmark"></i>
                    </button>
                    <div class="modal-content-group">
                        <p class="modal-message modal-message--error">确定要删除ID为{{SelectAlbumid}}的相册吗？请注意，当删除相册后，该相册内全部图片都将会被删除！</p>
                        <div class="modal-button-group">
                            <button class="modal-button modal-button--cancel" @click="closeDeleteAlbumModal">取消</button>
                            <button class="modal-button modal-button--danger" @click="confirmDeleteAlbum">确认删除</button>
                        </div>
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

        const SelectPhotoid = ref(0);
        const deletePhotoModalVisible = ref(false);

        const SelectAlbumid = ref(0);
        const deleteAlbumModalVisible = ref(false);


        const switchTab = (tab) => {
            activeTab.value = tab;
            currentPage.value = 1;
            fetchAll();
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
            fetchAll();
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

        const fetchAll = async () => {

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
                        console.error('获取数据失败:', data.message);
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

        // 打开删除照片确认框
        const openDeletePhotoModal = (photoid) => {
            SelectPhotoid.value = photoid;
            deletePhotoModalVisible.value = true;
        }

        // 关闭删除照片确认框
        const closeDeletePhotoModal = () => {
            SelectPhotoid.value = 0;
            deletePhotoModalVisible.value = false;
        }

        // 确认删除照片
        const confirmDeletePhoto = async () => {
            try {
                const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/api/del_user_photo`, {
                    photoid: SelectPhotoid.value
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
                } else {
                    alert(data);
                }
            } catch (e) {
                alert(e.message);
            } finally {
                refreshCache();
                closeDeletePhotoModal();
                location.reload();
            }
        };


        // 打开删除相册确认框
        const openDeleteAlbumModal = (Albumid) => {
            SelectAlbumid.value = Albumid;
            deleteAlbumModalVisible.value = true;
        }

        // 关闭删除相册确认框
        const closeDeleteAlbumModal = () => {
            SelectAlbumid.value = 0;
            deleteAlbumModalVisible.value = false;
        }

        //删除相册
        const confirmDeleteAlbum = async () => {
            try {
                const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/api/del_user_album`, {
                    albumid: SelectAlbumid.value
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
                } else {
                    alert(data);
                }
            } catch (e) {
                alert(e.message);
            } finally {
                closeDeleteAlbumModal();
                refreshCache();
            }
        };

        onMounted(() => {
            storedToken.value = localStorage.getItem("jwttoken");
            if (!storedToken.value) {
                alert("请先登录");
                router.push('/');
            }else{
                fetchAll();
            }
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

            openDeletePhotoModal,
            deletePhotoModalVisible,
            closeDeletePhotoModal,
            SelectPhotoid,
            confirmDeletePhoto,

            openDeleteAlbumModal,
            deleteAlbumModalVisible,
            closeDeleteAlbumModal,
            SelectAlbumid,
            confirmDeleteAlbum,

        };
    }
};
</script>

<style scoped></style>
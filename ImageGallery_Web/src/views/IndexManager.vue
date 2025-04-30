<template>
    <div class="container">
        <header class="header">
            <h1>{{ title }}</h1>
            <h2>{{ subtitle }}</h2>
            <div class="status-bar">
                <span v-if="isLoggedIn" class="username" @click="handleLogout">
                    {{ username }}
                </span>
                <button v-else class="status-button login-button" @click="showLoginModal">
                    登录
                </button>
                <button class="status-button mode-toggle-btn" @click="toggleDarkMode">
                    <i :class="DarkMode ? 'fa-solid fa-sun' : 'fa-solid fa-moon'"></i>
                </button>
            </div>
        </header>

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
                <div class="action-section">
                    <!-- <div class="comment-section" @click.stop="showCommentModal(photo.photoid)">
                        <i class="fa-regular fa-comment"></i>
                    </div> -->
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
            <div v-if="CommentModalVisible" class="comment-modal">
                <div class="modal-content">
                    <button @click="closeCommentModal" class="close-button" title="关闭">
                        <i class="fa-solid fa-xmark"></i>
                    </button>

                    <div class="comment-list">
                        <div v-for="comment in comments" :key="comment.commentid" class="comment-item">
                            <div class="comment-content">
                                <div class="comment-info">
                                    <span class="comment-username">{{ comment.username }}:</span>
                                    <span class="comment-text">{{ comment.content }}</span>
                                </div>
                                <div class="comment-actions">
                                    <button @click="toggleCommentLike(comment.commentid)" class="like-button">
                                        <i class="fa-regular fa-heart" :class="{ 'fa-solid': comment.isLiked }"></i>
                                        <span class="like-count">{{ comment.likes }}</span>
                                    </button>
                                </div>
                            </div>

                            <div v-if="comment.replies.length > 0" class="reply-list">
                                <div v-for="reply in comment.replies" :key="reply.commentid" class="reply-item">
                                    <div class="comment-info">
                                        <span class="comment-username"> {{ reply.username }}:</span>
                                        <span class="comment-text">{{ reply.content }}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="login-prompt">
                        <p>评论系统暂未开放</p>
                    </div>
                </div>
            </div>
        </transition>

        <transition name="fade">
            <div v-if="imageModalVisible" class="image-modal" @click="imageModalClick">
                <div class="modal-content" @click.stop>
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

        <transition name="fade">
            <div v-if="LoginModalVisible" class="login-modal">
                <div class="modal-content" @click.stop>
                    <h2>登录</h2>
                    <button @click="closeLoginModal" class="close-button" title="关闭">
                        <i class="fa-solid fa-xmark"></i>
                    </button>
                    <div class="input-group">
                        <label for="username">用户名</label>
                        <input id="username" type="text" v-model="loginUsername" placeholder="请输入用户名" />
                    </div>
                    <div class="input-group">
                        <label for="password">密码</label>
                        <input id="password" type="password" v-model="loginUsertoken" placeholder="请输入Token" />
                    </div>
                    <button @click="handleLogin">登录</button>
                    <p v-if="loginError" class="error">{{ loginError }}</p>
                    <div>
                        <p class="register-hint">
                            没有账号？<a href="#" @click.prevent="openRegModal" class="register-link">注册</a>
                        </p>
                    </div>
                </div>
            </div>
        </transition>

        <transition name="fade">
            <div v-if="RegModalVisible" class="login-modal">
                <div class="modal-content" @click.stop>
                    <h2>注册</h2>
                    <button @click="closeRegModal" class="close-button" title="关闭">
                        <i class="fa-solid fa-xmark"></i>
                    </button>
                    <div class="input-group">
                        <label for="username">用户名</label>
                        <input id="username" type="text" v-model="RegUsername" placeholder="请输入用户名" />
                    </div>
                    <div class="input-group">
                        <label for="password1">密码</label>
                        <input id="password1" type="password" v-model="RegPasswd1" placeholder="请输入密码" />
                    </div>
                    <div class="input-group">
                        <label for="password2">重复密码</label>
                        <input id="password2" type="password" v-model="RegPasswd2" placeholder="请再次输入密码" />
                    </div>
                    <button @click="handleReg">注册</button>
                    <p v-if="RegError" class="error">{{ RegError }}</p>
                </div>
            </div>
        </transition>

        <transition name="fade">
            <div v-if="RegSuccModalVisible" class="login-modal">
                <div class="modal-content" @click.stop>
                    <h2>注册成功</h2>
                    <button @click="closeRegModal" class="close-button" title="关闭">
                        <i class="fa-solid fa-xmark"></i>
                    </button>
                    <div class="input-group">
                        <p class="success">3s后准备自动登录...</p>
                    </div>
                </div>
            </div>
        </transition>
        <br />
        <br />
        <footer class="custom-footer">
            <div class="footer-content">
                <p>
                    Powered by
                    <a href="https://github.com/yanhy2000/ImageGallery" target="_blank">ImageGallery</a>
                </p>
                <p>{{ displayContent }}</p>
                <p>Copyright © <span id="footer-year"></span> yanhy2000</p>
            </div>
        </footer>
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

export default {
    name: "IndexManager",
    setup() {
        const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
        const title = import.meta.env.VITE_APP_TITLE;
        const subtitle = import.meta.env.VITE_APP_SUBTITLE;
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

        const isLoggedIn = ref(false);
        const username = ref("");
        const LoginModalVisible = ref(false);
        const loginUsername = ref("");
        const loginUsertoken = ref("");
        const loginError = ref("");

        const RegSuccModalVisible = ref(false);
        const RegModalVisible = ref(false);
        const RegUsername = ref("");
        const RegPasswd1 = ref("");
        const RegPasswd2 = ref("");
        const RegError = ref("");

        const newComment = ref("");
        const replyText = ref("");

        const CommentModalVisible = ref(false);
        const totalPhotos = ref(0);
        const perPageOptions = [6, 9, 15, 20, 25, 30];
        const error = ref(null);
        const DarkMode = ref(false);
        const isTooltipVisible = ref(false);
        const config = ref({
            version: "1.0.4",
            customContent: import.meta.env.VITE_API_FOOTER_CONTENT,
        });
        const year = new Date().getFullYear();

        const displayContent = computed(() => {
            return config.value.customContent
                ? `${config.value.customContent} V${config.value.version}`
                : `${title.value}  V${config.value.version}`;
        });

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

        const submitComment = () => {
            if (newComment.value.trim()) {
                comments.value.push({
                    commentid: comments.value.length + 1,
                    content: newComment.value,
                    create_time: new Date().toLocaleString(),
                    userid: props.currentUser.userid,
                    username: props.currentUser.username,
                    likes: 0,
                    isLiked: false,
                    replies: [],
                });
                newComment.value = "";
            }
        };

        const submitReply = (commentid) => {
            if (replyText.value.trim()) {
                const comment = comments.value.find((c) => c.commentid === commentid);
                if (comment) {
                    comment.replies.push({
                        commentid: comment.replies.length + 1,
                        content: replyText.value,
                        create_time: new Date().toLocaleString(),
                        userid: props.currentUser.userid,
                        username: props.currentUser.username,
                    });
                    replyText.value = "";
                }
            }
        };

        const toggleCommentLike = (commentid) => {
            const comment = comments.value.find((c) => c.commentid === commentid);
            if (comment) {
                comment.isLiked = !comment.isLiked;
                comment.likes += comment.isLiked ? 1 : -1;
            }
        };

        const deleteComment = (commentid) => {
            comments.value = comments.value.filter((c) => c.commentid !== commentid);
        };

        const showCommentModal = (photoid) => {
            CommentModalVisible.value = true;
        };

        const closeCommentModal = () => {
            CommentModalVisible.value = false;
        };

        const comments = ref([
            {
                commentid: 1,
                content: "这是一条示例评论。",
                create_time: "2023-10-01 12:00",
                userid: 1,
                username: "用户A",
                likes: 11,
                isLiked: false,
                replies: [
                    {
                        commentid: 2,
                        content: "这是一条回复评论。",
                        create_time: "2023-10-01 12:05",
                        userid: 2,
                        username: "用户B",
                    },
                ],
            },
            {
                commentid: 3,
                content: "这是另一条示例评论。",
                create_time: "2023-10-01 12:10",
                userid: 3,
                username: "用户C",
                likes: 5,
                isLiked: false,
                replies: [],
            },
        ]);

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
                    LoginModalVisible.value ||
                    CommentModalVisible.value)
            ) {
                imageModalVisible.value = false;
                LoginModalVisible.value = false;
                CommentModalVisible.value = false;
            }
        };

        const imageModalClick = (event) => {
            if (event.target === event.currentTarget) {
                imageModalVisible.value = false;
            }
        };

        const toggleDarkMode = () => {
            DarkMode.value = !DarkMode.value;
            if (DarkMode.value) {
                document.body.classList.add("dark-mode");
            } else {
                document.body.classList.remove("dark-mode");
            }
        };

        const checkDarkMode = () => {
            const prefersDarkMode = window.matchMedia("(prefers-color-scheme: dark)");
            if (prefersDarkMode.matches) {
                DarkMode.value = true;
                document.body.classList.add("dark-mode");
            } else {
                DarkMode.value = false;
                document.body.classList.remove("dark-mode");
            }
            prefersDarkMode.addEventListener("change", () => { });
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

        const showLoginModal = () => {
            LoginModalVisible.value = true;
        };

        const closeLoginModal = () => {
            LoginModalVisible.value = false;
            loginError.value = "";
        };

        const loginModalClick = (event) => {
            if (event.target === event.currentTarget) {
                LoginModalVisible.value = false;
            }
        };

        // 处理登录
        const handleLogin = async () => {
            try {
                const response = await axios.post(
                    `${import.meta.env.VITE_API_BASE_URL}/api/checktoken`,
                    {
                        username: loginUsername.value,
                        usertoken: loginUsertoken.value,
                    }
                );

                if (response.data.code === 200 && response.data.data.allowlogin) {
                    isLoggedIn.value = true;
                    username.value = loginUsername.value;
                    localStorage.setItem("jwttoken", response.data.data.token);
                    localStorage.setItem("username", loginUsername.value);
                    closeLoginModal();
                    location.reload();
                } else if (
                    response.data.code === 200 &&
                    !response.data.data.allowlogin
                ) {
                    loginError.value = "用户已被封禁，请联系管理员";
                } else {
                    loginError.value = "登录失败，请检查用户名和 Token";
                }
            } catch (error) {
                loginError.value = "登录失败，请稍后重试";
            }
        };

        const handleLogout = () => {
            isLoggedIn.value = false;
            username.value = "";
            localStorage.removeItem("jwttoken");
            localStorage.removeItem("username");
            location.reload();
        };

        // 注册逻辑
        const openRegModal = () => {
            closeLoginModal();
            RegModalVisible.value = true;
            RegError.value = "";
        };

        const closeRegModal = () => {
            RegModalVisible.value = false;
            RegError.value = "";
        };

        const handleRegisterError = (code) => {
            switch (code) {
                case 400:
                    RegError.value = "用户名已存在";
                    break;
                case 401:
                    RegError.value = "接口未传入用户名或密码";
                    break;
                case 402:
                    RegError.value = "密码不符合要求";
                    break;
                case 403:
                    RegError.value = "用户名不符合要求";
                    break;
                case 404:
                    RegError.value = "服务器未开放注册";
                    break;
                default:
                    RegError.value = `注册失败 (错误码: ${code})`;
            }
        };

        const handleReg = async () => {
            if (RegPasswd1.value != "" && RegPasswd2.value != "") {
                if (RegPasswd1.value != RegPasswd2.value) {
                    RegError.value = "两次输入的密码不一致！";
                    RegPasswd2.value = "";
                    return;
                } else {
                    const reg_pass = /^[a-zA-Z0-9]{6,20}$/;
                    const reg_user = /^[_0-9a-zA-Z][a-zA-Z0-9_]{3,16}$/;
                    if (!reg_pass.test(RegPasswd1.value)) {
                        RegError.value = "密码必须为6-20位字母或数字！";
                        RegPasswd2.value = "";
                        return;
                    }
                    if (!reg_user.test(RegUsername.value)) {
                        RegError.value = "用户名必须为4-16位字母或数字或下划线！";
                        RegUsername.value = "";
                        RegPasswd1.value = "";
                        RegPasswd2.value = "";
                        return;
                    }
                }
            }
            try {
                const response = await axios.post(
                    `${import.meta.env.VITE_API_BASE_URL}/api/register`,
                    {
                        username: RegUsername.value,
                        usertoken: RegPasswd1.value,
                    }
                );
                if (response.data.code === 200) {
                    closeRegModal();
                    RegSuccModalVisible.value = true;
                    setTimeout(() => {
                        loginUsername.value = RegUsername.value;
                        loginUsertoken.value = RegPasswd1.value;
                        handleLogin();
                        RegSuccModalVisible.value = false;
                    }, 3000);
                }
            } catch (error) {
                if (error.response) {
                    handleRegisterError(error.response.data.code);
                } else {
                    RegError.value = '注册失败，请联系管理员或稍后重试';
                }
            }
        };

        onMounted(async () => {
            const storedToken = localStorage.getItem("jwttoken");
            const storedUsername = localStorage.getItem("username");

            if (storedToken && storedUsername) {
                try {
                    const response = await axios.get(
                        `${import.meta.env.VITE_API_BASE_URL}/api/protected`,
                        {
                            headers: {
                                Authorization: `Bearer ${storedToken}`,
                            },
                        }
                    );

                    if (response.data.code === 200) {
                        isLoggedIn.value = true;
                        username.value = storedUsername;
                    } else if (response.data.code === 403) {
                        localStorage.removeItem("jwttoken");
                        localStorage.removeItem("username");
                        alert("用户已被封禁，请重新登录");
                    } else {
                        localStorage.removeItem("jwttoken");
                        localStorage.removeItem("username");
                    }
                } catch (error) {
                    alert("自动登录失败, Token 无效或过期", error);
                    localStorage.removeItem("jwttoken");
                    localStorage.removeItem("username");
                }
            }

            const isMobile = window.innerWidth <= 768;
            if (isMobile) {
                perPage.value = 6;
            }
            await fetchPhotos();
            await checkUserLikes();
            checkDarkMode();
            await cleanExpiredPhotos();
            const link = document.createElement("link");
            link.rel = "icon";
            link.href = "img/favicon.ico";

            document.head.appendChild(link);
            document.addEventListener("keydown", handleEscKey);
            document.getElementById("footer-year").innerText = year;
        });

        onBeforeUnmount(() => {
            document.removeEventListener("keydown", handleEscKey);
        });

        return {
            API_BASE_URL,
            title,
            subtitle,
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

            isLoggedIn,
            username,
            LoginModalVisible,
            loginUsername,
            loginUsertoken,
            loginError,
            showLoginModal,
            closeLoginModal,
            handleLogin,
            handleLogout,

            openRegModal,
            closeRegModal,
            RegUsername,
            RegError,
            RegPasswd1,
            RegPasswd2,
            RegModalVisible,
            RegSuccModalVisible,
            handleReg,

            comments,
            newComment,
            replyText,
            submitComment,
            submitReply,
            toggleCommentLike,
            deleteComment,
            showCommentModal,
            closeCommentModal,
            CommentModalVisible,

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
@import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css");
@import "@/css/index.css";
@import "@/css/image-modal.css";
@import "@/css/login-modal.css";
@import "@/css/pagination.css";
@import "@/css/btn.css";
@import "@/css/action.css";
@import "@/css/status-bar.css";
@import "@/css/action-modal.css";
@import "@/css/comment.css";
</style>

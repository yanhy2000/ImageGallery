<template>
    <div v-if="isLoggedIn" class="user-menu-container">
        <span class="username" @click="AccountManager">
            {{ username }}
            <i class="fa-solid fa-caret-down"></i>
        </span>
        <div class="dropdown-menu">
            <button class="dropdown-item" @click="UploadManager">
                <i class="fa-solid fa-upload"></i> 上传照片
            </button>
            <button class="dropdown-item" @click="AccountManager">
                <i class="fa-solid fa-user-gear"></i> 账户管理
            </button>
            <button class="dropdown-item" @click="handleLogout">
                <i class="fa-solid fa-right-from-bracket"></i> 注销
            </button>
        </div>
    </div>

    <button v-else class="status-button login-button" @click="showLoginModal">
        登录
    </button>

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
</template>

<script>
import { ref, onMounted, } from "vue";
import { useRouter } from 'vue-router';
import axios from "axios";

export default {
    name: "IndexManager",
    setup() {
        const isLoggedIn = ref(false);
        const username = ref("");
        const router = useRouter();
        const UploadManager = () => router.push('/upload');
        const AccountManager = () => router.push('/account');

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




        const showLoginModal = () => {
            LoginModalVisible.value = true;
        };

        const closeLoginModal = () => {
            LoginModalVisible.value = false;
            loginError.value = "";
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
                    RegError.value = "请输入用户名和密码";
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
                    RegError.value = `注册失败，请联系管理员或稍后重试${error}`;
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
                    // alert("自动登录失败, Token 无效或过期", error);
                    localStorage.removeItem("jwttoken");
                    localStorage.removeItem("username");
                }
            }

        });

        return {
            UploadManager,
            AccountManager,
            isLoggedIn,
            username,

            showLoginModal,
            isLoggedIn,
            username,
            LoginModalVisible,
            loginUsername,
            loginUsertoken,
            loginError,
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
        };
    },
};
</script>

<style></style>

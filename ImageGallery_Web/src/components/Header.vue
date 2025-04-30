<template>
    <header class="header">
        <h1>{{ title }}</h1>
        <h2>{{ subtitle }}</h2>
        <div class="status-bar">
            <Login />
            <button class="status-button mode-toggle-btn" @click="toggleDarkMode">
                <i :class="DarkMode ? 'fa-solid fa-sun' : 'fa-solid fa-moon'"></i>
            </button>
        </div>
    </header>
</template>

<script>
import { ref, onMounted, } from "vue";
import { useRouter } from 'vue-router';
import Login from './Login.vue'

export default {
    name: "IndexManager",
    components: { Login },
    setup() {
        const title = import.meta.env.VITE_APP_TITLE;
        const subtitle = import.meta.env.VITE_APP_SUBTITLE;
        const DarkMode = ref(false);

        const router = useRouter();
        const UploadManager = () => router.push('/upload');
        const AccountManager = () => router.push('/account');

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


        onMounted(async () => {

            checkDarkMode();
        });

        return {
            title,
            subtitle,
            UploadManager,
            AccountManager,
            DarkMode,
            toggleDarkMode,

        };
    },
};
</script>

<style></style>

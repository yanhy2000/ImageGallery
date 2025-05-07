<template>
        <br />
        <br />
        <footer class="custom-footer">
            <div class="footer-content">
                <p>
                    Powered by
                    <a href="https://github.com/yanhy2000/ImageGallery" target="_blank">ImageGallery</a>
                </p>
                <p><span id="displayContent"></span></p>
                <p>Copyright © <span id="footer-year"></span> yanhy2000</p>
            </div>
        </footer>
</template>
<script>
import { ref, onMounted, computed } from "vue";
export default {
    name: "IndexManager",
    setup() {
        const config = ref({
            version: "1.1.2",
            customContent: import.meta.env.VITE_API_FOOTER_CONTENT,
        });
        const year = new Date().getFullYear();
        const displayContent = computed(() => {
            return config.value.customContent
                ? `${config.value.customContent} V${config.value.version}`
                : `${title.value}  V${config.value.version}`;
        });

        onMounted(async () => {
            document.getElementById("footer-year").innerText = year;
            document.getElementById("displayContent").innerText = displayContent.value;
        });
        
        return {
        };
    },
};
</script>
<style>
</style>

import { ref } from 'vue';

export function useModalManager() {
    const imageModalVisible = ref(false);
    const LoginModalVisible = ref(false);
    const currentImage = ref(null);
    const currentThumbnailUrl = ref(null);

    const openImageModal = () => {
        imageModalVisible.value = true;
    };

    const closeImageModal = () => {
        imageModalVisible.value = false;
        currentImage.value = null;
        currentThumbnailUrl.value = null;
    };

    const showLoginModal = () => {
        LoginModalVisible.value = true;
    };

    const closeLoginModal = () => {
        LoginModalVisible.value = false;
    };

    const loginModalClick = (event) => {
        if (event.target === event.currentTarget) {
            LoginModalVisible.value = false;
        }
    };

    const imageModalClick = (event) => {
        if (event.target === event.currentTarget) {
            imageModalVisible.value = false;
        }
    };

    return {
        imageModalVisible,
        LoginModalVisible,
        currentImage,
        currentThumbnailUrl,
        openImageModal,
        closeImageModal,
        showLoginModal,
        closeLoginModal,
        loginModalClick,
        imageModalClick,
    };
}
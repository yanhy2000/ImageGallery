<template>
  <div class="container">
    <Header />
    <div class="back-home-container">
      <button class="back-home" @click="handleBackToHome">
        <i class="fa-solid fa-house"></i> 返回主页
      </button>
    </div>
    <main class="upload-container">
      <div class="upload-area" :class="{ 'drag-active': isDragging, 'hidden': fileSelected }" @click="triggerFileInput"
        @dragover.prevent="handleDragOver" @dragleave="handleDragLeave" @drop.prevent="handleDrop">
        <div class="upload-content">
          <i class="fas fa-plus upload-icon"></i>
          <p class="upload-text">点击或拖拽图片到此处上传</p>
          <p class="upload-hint">支持 JPG/PNG/GIF 格式，最大 20MB</p>
        </div>
        <input type="file" ref="fileInput" class="file-input" accept="image/jpeg,image/png,image/gif"
          @change="handleFileChange">
      </div>

      <!-- 错误提示 -->
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <!-- 上传表单 (文件选择后显示) -->
      <transition name="fade">
        <div v-if="fileSelected" class="upload-form">
          <div class="file-preview">
            <img v-if="previewUrl" :src="previewUrl" alt="预览" class="preview-image">
            <div class="file-info">
              <h3>{{ fileName }}</h3>
              <p>{{ fileSize }} MB</p>
            </div>
          </div>

          <div class="form-group">
            <label for="description">照片描述</label>
            <textarea id="description" v-model="description" placeholder="请输入照片描述" rows="3"></textarea>
          </div>

          <div class="form-group">
            <label for="album">相册</label>
            <input type="text" id="album" v-model="album" placeholder="默认使用用户名作为相册">
          </div>

          <button class="upload-button" @click="submitUpload" :disabled="isUploading">
            <span v-if="!isUploading">上传照片</span>
            <span v-else class="uploading-text">
              <i class="fas fa-spinner fa-spin"></i> 上传中...
            </span>
          </button>
        </div>
      </transition>

      <transition name="fade">
        <div v-if="SuccModalVisible" class="modal-overlay">
          <div class="modal-content modal-content--small">
            <h2 class="modal-title">{{ Upload_status }}</h2>
            <div class="modal-content-group">
              <p class="modal-message modal-message--success">2s后返回主页...</p>
            </div>
          </div>
        </div>
      </transition>


    </main>
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
  refreshCache,
} from "@/services/cacheService";
export default {
  components: { Header, Foot },
  setup() {
    const router = useRouter();
    const SuccModalVisible = ref(false);
    const Upload_status = ref("上传状态");
    const fileInput = ref(null);
    const isDragging = ref(false);
    const fileSelected = ref(false);
    const errorMessage = ref('');
    const isUploading = ref(false);

    const storedToken = ref("");

    const selectedFile = ref(null);
    const previewUrl = ref('');
    const fileName = ref('');
    const fileSize = ref(0);

    const description = ref('');
    const album = ref('');

    const handleBackToHome = () => router.push('/');

    const triggerFileInput = () => {
      fileInput.value.click();
    };

    const handleDragOver = () => {
      isDragging.value = true;
    };

    const handleDragLeave = () => {
      isDragging.value = false;
    };

    const handleDrop = (e) => {
      isDragging.value = false;
      const files = e.dataTransfer.files;
      if (files.length) {
        validateAndSetFile(files[0]);
      }
    };

    const handleFileChange = (e) => {
      const files = e.target.files;
      if (files.length) {
        validateAndSetFile(files[0]);
      }
    };

    const validateAndSetFile = (file) => {
      errorMessage.value = '';

      const validTypes = ['image/jpeg', 'image/png', 'image/gif'];
      if (!validTypes.includes(file.type)) {
        errorMessage.value = '只支持 JPG/PNG/GIF 格式的图片';
        return;
      }

      const maxSize = 20 * 1024 * 1024; // 20MB
      if (file.size > maxSize) {
        errorMessage.value = '文件大小不能超过 20MB';
        return;
      }

      selectedFile.value = file;
      fileName.value = file.name;
      fileSize.value = (file.size / (1024 * 1024)).toFixed(2);

      previewUrl.value = URL.createObjectURL(file);
      fileSelected.value = true;
    };


    const HandleUpload = async () => {
      if (!selectedFile.value) return;

      try {
        isUploading.value = true;

        if (!storedToken.value) {
          throw new Error("请先登录");
        }

        const formData = new FormData();
        formData.append('file', selectedFile.value);
        formData.append('desc', description.value || '无描述');
        formData.append('album', album.value);

        const response = await axios.post(
          `${import.meta.env.VITE_API_BASE_URL}/api/uploadphoto`,
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
              'Authorization': `Bearer ${storedToken.value}`
            }
          }
        );

        if (response.data.code === 200) {
          Upload_status.value = "上传成功"
          SuccModalVisible.value = true;
          refreshCache(false);
          setTimeout(() => {
            resetForm();
            SuccModalVisible.value = false;
            router.push('/');
          }, 2000);
        } else {
          Upload_status.value = "上传失败"
          SuccModalVisible.value = true;
          setTimeout(() => {
            resetForm();
            SuccModalVisible.value = false;
            router.push('/');
          }, 2000);
          throw new Error(response.data.message || '上传失败');
        }
      } catch (error) {
        console.error('上传失败:', error);
        errorMessage.value = error.message || '上传失败，请稍后重试';
      } finally {
        isUploading.value = false;
      }
    };

    const resetForm = () => {
      fileSelected.value = false;
      selectedFile.value = null;
      previewUrl.value = '';
      fileName.value = '';
      fileSize.value = 0;
      description.value = '';
      album.value = '';
      errorMessage.value = '';

      if (fileInput.value) {
        fileInput.value.value = '';
      }
    };

    onMounted(() => {
      storedToken.value = localStorage.getItem("jwttoken");
      if (!storedToken.value) {
        alert("请先登录");
        router.push('/');
      }
    });

    return {
      fileInput,
      isDragging,
      fileSelected,
      errorMessage,
      isUploading,
      previewUrl,
      fileName,
      fileSize,
      description,
      album,
      triggerFileInput,
      handleDragOver,
      handleDragLeave,
      handleDrop,
      handleFileChange,
      submitUpload: HandleUpload,
      SuccModalVisible,
      Upload_status,
      handleBackToHome,
    };
  }
};
</script>

<style scoped>
@import "@/css/upload-page.css";
</style>
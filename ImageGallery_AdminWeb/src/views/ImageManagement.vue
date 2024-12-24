<template>
  <div class="image-management">
    <h1>图片管理</h1>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-else>
      <table class="photo-table">
        <thead>
          <tr>
            <th>图片ID</th>
            <th>名称</th>
            <th>描述</th>
            <th>上传时间</th>
            <th>缩略图</th>
            <th>图片链接</th>
            <th>相册名称</th>
            <th>相册ID</th>
            <th>用户ID</th>
            <th>用户名</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="photo in photos" :key="photo.photoid">
            <td>{{ photo.photoid }}</td>
            <td>{{ photo.name }}</td>
            <td><button @click="_showModifyDescModal(photo)">修改</button> {{ photo.desc }} </td>
            <td>{{ photo.upload_time }}</td>
            <td><img :src="photo.thumbnail" :alt="photo.name" class="thumbnail"></td>
            <td>
              <button @click="downloadImage(photo.photoid)">下载原图</button>
            </td>
            <td>{{ photo.album_name }}</td>
            <td>{{ photo.albumid }}</td>
            <td>{{ photo.userid }}</td>
            <td>{{ photo.username }}</td>
            <td><button @click="_showDeletePhotoModal(photo)">删除</button></td>
          </tr>
        </tbody>
      </table>

      <div v-if="showModifyDescModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeModal">&times;</span>
        <p>填写ID为 {{ selectedPhoto.photoid }} 的图片描述：</p>
        <input type="text" v-model="selectedPhoto.desc">
        <button @click="ModifyDesc(selectedPhoto)">确定</button>
        <button @click="closeModal">取消</button>
      </div>
    </div>
      <div v-else-if="showDeletePhotoModal" class="modal">
        <div class="modal-content">
        <span class="close" @click="closeModal">&times;</span>
        <p>确定要删除ID为 {{ selectedPhoto.photoid }} 的图片？</p>
        <button @click="DeletePhoto(selectedPhoto)">确定</button>
        <button @click="closeModal">取消</button>
      </div>
      </div>
    </div>
    
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';



export default {
  name: 'ImageManagement',
  setup() {
    const photos = ref([]);
    const error = ref(null);
    const selectedPhoto = ref({});
    const showModifyDescModal = ref(false);
    const showDeletePhotoModal = ref(false);

    
    const fetchImages = async () => {
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/api/photolist`, {
          page: 1,
          perpage: 10
        }, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${import.meta.env.VITE_ADMIN_TOKEN}`
          }
        });

        if (response.status !== 200) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = response.data;

        if (data.code === 200) {
          photos.value = data.data.photos;
        } else {
          error.value = data.message;
        }
      } catch (e) {
        error.value = e.message;
      }
    };

    const ModifyDesc = async (photo) => {
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/api/updatephoto`, {
          photoid: photo.photoid,
          desc: photo.desc
        }, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${import.meta.env.VITE_ADMIN_TOKEN}`
          }
        });

        if (response.status !== 200) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = response.data;
        if (data.code === 200) {
          fetchImages();
        } else {
          alert(data.message);
        }
      } catch (e) {
        alert(e.message); 
      } finally {
        closeModal();
      }
    };

    const DeletePhoto = async (photo) => {
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/api/deletephoto`, {
          photoid: photo.photoid
        }, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${import.meta.env.VITE_ADMIN_TOKEN}`
          }
        });

        if (response.status !== 200) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = response.data;

        if (data.code === 200) {
          fetchImages();
        } else {
          alert(data);
        }
      } catch (e) {
        alert(e.message);
      } finally {
        closeModal();
      }
    };

    const _showModifyDescModal = (photo) => {
      selectedPhoto.value = photo;
      showModifyDescModal.value = true;
    };

    const _showDeletePhotoModal = (photo) => {
      selectedPhoto.value = photo;
      showDeletePhotoModal.value = true;
    };

    const closeModal = () => {
      showDeletePhotoModal.value = false;
      showModifyDescModal.value = false;
      selectedPhoto.value = {};
    };



    onMounted(fetchImages);

    return { 
      photos, 
      error,
      selectedPhoto,
      showModifyDescModal,
      showDeletePhotoModal,
      _showModifyDescModal,
      _showDeletePhotoModal,
      closeModal,
      ModifyDesc,
      DeletePhoto
     };
  },
  methods: {
    downloadImage(photoid) {
      console.log(photoid);
      const downloadUrl = `${import.meta.env.VITE_API_BASE_URL}/api/getphoto?photoid=${photoid}&thumbnail=1`;
      window.location.href = downloadUrl;
    }
  }
};
</script>

<style scoped>
.image-management {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

.error {
  color: red;
  text-align: center;
  margin-bottom: 20px;
}

.photo-table {
  width: 100%;
  border-collapse: collapse;
}

.photo-table th,
.photo-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.photo-table th {
  background-color: #f2f2f2;
  font-weight: bold;
}

.thumbnail {
  width: 100px;
  height: auto;
}

a {
  color: #007bff;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

button {
  padding: 8px 16px;
  margin-top: 8px;
  margin-right: 8px;
}

.modal {
  display: block;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}
</style>
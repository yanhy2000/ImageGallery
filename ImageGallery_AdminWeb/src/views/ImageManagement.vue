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
          </tr>
        </thead>
        <tbody>
          <tr v-for="photo in photos" :key="photo.photoid">
            <td>{{ photo.photoid }}</td>
            <td>{{ photo.name }}</td>
            <td>{{ photo.desc }}</td>
            <td>{{ photo.upload_time }}</td>
            <td><img :src="photo.thumbnail" :alt="photo.name" class="thumbnail"></td>
            <td>
              <button @click="downloadImage(photo.photoid)">下载原图</button>
            </td>
            <td>{{ photo.album_name }}</td>
            <td>{{ photo.albumid }}</td>
            <td>{{ photo.userid }}</td>
            <td>{{ photo.username }}</td>
          </tr>
        </tbody>
      </table>
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


    onMounted(fetchImages);

    return { photos, error };
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
</style>
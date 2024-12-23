<template>
  <div class="album-management">
    <h1>相册管理</h1>
    <table>
      <thead>
        <tr>
          <th>相册ID</th>
          <th>相册名称</th>
          <th>描述</th>
          <th>用户ID</th>
          <th>创建时间</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="album in albums" :key="album.albumid">
          <td>{{ album.albumid }}</td>
          <td>{{ album.name }}</td>
          <td>{{ album.description }}</td>
          <td>{{ album.userid }}</td>
          <td>{{ album.create_time }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>


<script>
import { ref } from 'vue';
import axios from 'axios';

export default {
  setup() {
    const albums = ref([]);
    const error = ref(null);

    const fetchAlbums = async () => {
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/api/albumlist`, {
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
          albums.value = data.data.albums;
        } else {
          error.value = data.message;
        }
      } catch (e) {
        error.value = e.message;
      }
    };

    fetchAlbums();

    return { albums, error };
  }
};
</script>

<style scoped>
.album-management table {
  width: 100%;
  border-collapse: collapse;
}

.album-management th,
.album-management td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.album-management th {
  background-color: #f2f2f2;
  color: #333;
}

.album-management tr:nth-child(even) {
  background-color: #f9f9f9;
}

</style>
<template>
  <div class="album-management">
    <h1>相册管理</h1>
    <table>
      <thead>
        <tr>
          <th>相册ID</th>
          <th>相册名称</th>
          <th>用户ID</th>
          <th>创建时间</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="album in albums" :key="album.albumid">
          <td>{{ album.albumid }}</td>
          <td><button @click="_showModifyNameModal(album)">修改</button> {{ album.name }}</td>
          <td>{{ album.userid }}</td>
          <td>{{ album.create_time }}</td>
          <td><button @click="_showDeleteAlbumModal(album)">删除</button></td>
        </tr>
      </tbody>
    </table>

    <div v-if="showModifyNameModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeModal">&times;</span>
        <p>填写ID为 {{ selectedAlbum.photoid }} 的相册名：</p>
        <input type="text" v-model="selectedAlbum.name">
        <button @click="ModifyName(selectedAlbum)">确定</button>
        <button @click="closeModal">取消</button>
      </div>
    </div>
      <div v-else-if="showDeleteAlbumModal" class="modal">
        <div class="modal-content">
        <span class="close" @click="closeModal">&times;</span>
        <p>确定要删除ID为 {{ selectedAlbum.albumid }} 的相册？删除相册会删除该相册下所有照片。</p>
        <button @click="DeleteAlbum(selectedAlbum)">确定</button>
        <button @click="closeModal">取消</button>
      </div>
      </div>
      <div class="pagination">
      <button @click="changePage('first')" :disabled="currentPage <= 1">首页</button>
      <button @click="changePage('prev')" :disabled="currentPage <= 1">上一页</button>
      <span>第 {{ currentPage }} 页，共 {{ totalPages }} 页</span>
      <button @click="changePage('next')" :disabled="currentPage >= totalPages">下一页</button>
      <button @click="changePage('last')" :disabled="currentPage >= totalPages">尾页</button>
    </div>
    <div class="per-page-selector">
      <label for="perPageSelect">每页展示数量：</label>
      <select id="perPageSelect" v-model="perPage" @change="fetchAlbums">
        <option v-for="option in perPageOptions" :key="option" :value="option">{{ option }}</option>
      </select>
    </div>
    </div>
</template>


<script>
import { ref } from 'vue';
import axios from 'axios';

export default {
  setup() {
    const albums = ref([]);
    const error = ref(null);
    const selectedAlbum = ref(null);
    const showModifyNameModal = ref(false);
    const showDeleteAlbumModal = ref(false);

    const currentPage = ref(1);
    const perPage = ref(10);
    const perPageOptions = [5, 10, 20, 50]; 
    const totalAlbums = ref(0); 
    const totalPages = ref(0);

    const changePage = (action) => {
      if (action === 'first') {
        currentPage.value = 1;
      } else if (action === 'prev' && currentPage.value > 1) {
        currentPage.value--;
      } else if (action === 'next' && currentPage.value < totalPages.value) {
        currentPage.value++;
      } else if (action === 'last') {
        currentPage.value = totalPages.value;
      }
      albums.value = [];
      fetchAlbums();
    };

    const fetchAlbums = async () => {
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/api/albumlist?page=${currentPage.value}&perpage=${perPage.value}`, {
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
          totalAlbums.value = data.data.totalAlbums;
          totalPages.value = data.data.totalPages;
        } else {
          error.value = data.message;
        }
      } catch (e) {
        error.value = e.message;
      }
    };

    const ModifyName = async (album) => {
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/api/setalbum`, {
          albumid: album.albumid,
          name: album.name
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
          fetchAlbums();
        } else {
          alert(data.message);
        }
      } catch (e) {
        alert(e.message); 
      } finally {
        closeModal();
      }
    };

    const DeleteAlbum = async (album) => {
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/api/deletealbum`, {
          albumid: album.albumid
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
          fetchAlbums();
        } else {
          alert(data);
        }
      } catch (e) {
        alert(e.message);
      } finally {
        closeModal();
      }
    };

    const _showModifyNameModal = (albums) => {
      selectedAlbum.value = albums;
      showModifyNameModal.value = true;
    };

    const _showDeleteAlbumModal = (albums) => {
      selectedAlbum.value = albums;
      showDeleteAlbumModal.value = true;
    };

    const closeModal = () => {
      showDeleteAlbumModal.value = false;
      showModifyNameModal.value = false;
      selectedAlbum.value = {};
    };

    fetchAlbums();

    return { 
      albums, 
      error, 
      selectedAlbum, 
      showModifyNameModal, 
      showDeleteAlbumModal, 
      _showModifyNameModal, 
      _showDeleteAlbumModal, 
      closeModal,
      ModifyName,
      DeleteAlbum,
      changePage,
      currentPage,
      perPage,
      perPageOptions,
      totalAlbums,
      totalPages,
      fetchAlbums
     };
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
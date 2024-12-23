<template>
  <div class="user-management">
    <h1>用户管理</h1>
    <button @click="showAddUserModal">新增用户</button>
    <table>
      <thead>
        <tr>
          <th>用户ID</th>
          <th>用户名</th>
          <th>权限</th>
          <th>用户令牌</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(user, index) in users" :key="user.userid">
          <td>{{ user.userid }}</td>
          <td>{{ user.username }}</td>
          <td>{{ permissionText(user.permissions) }}</td>
          <td>{{ user.usertoken }}</td>
          
          <td v-if="index !== 0">
            <button @click="prepareRegenToken(user)">重新生成token</button>
            <button @click="prepareBanUser(user)">封禁/解禁用户</button>
            <button @click="showDeleteUserModal(user)">删除用户</button>
          </td>
          <td v-else>
            <button @click="prepareRegenToken(user)">重新生成token</button>
            <a> 管理员账号，不可删除 </a>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="showRegenTokenModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeRegenTokenModal">&times;</span>
        <p>确定要重新生成用户 {{ selectedUser.username }} 的用户令牌吗？</p>
        <button @click="regentoken(selectedUser)">确定</button>
        <button @click="closeRegenTokenModal">取消</button>
      </div>
    </div>

    <div v-if="showBanModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeBanModal">&times;</span>
        <p>您确定要 {{ banActionText() }} 用户 {{ selectedUser.username }} 吗？</p>
        <button @click="toggleBan(selectedUser)">确定</button>
        <button @click="closeBanModal">取消</button>
      </div>
    </div>

    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeModal">&times;</span>
        <p v-if="modalType === 'add'">请输入用户名：</p>
        <p v-else>确定删除用户 {{ selectedUser.username }}?</p>
        <input v-if="modalType === 'add'" v-model="newUsername" type="text" placeholder="用户名">
        <button v-if="modalType === 'add'" @click="addUser">提交</button>
        <button v-else @click="deleteUser">确定</button>
        <button @click="closeModal">取消</button>
      </div>
    </div>
  </div>
</template>


<script>
import { ref } from 'vue';
import axios from 'axios';

export default {
  setup() {
    const users = ref([]);
    const error = ref(null);
    const showModal = ref(false);
    const modalType = ref('');
    const newUsername = ref('');
    const selectedUser = ref({});
    const showBanModal = ref(false);
    const showRegenTokenModal = ref(false);

    const fetchUsers = async () => {
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/api/userlist`, {
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
          users.value = data.data.users;
        } else {
          error.value = data.message;
        }
      } catch (e) {
        error.value = e.message;
      }
    };
    const showAddUserModal = () => {
      modalType.value = 'add';
      showModal.value = true;
    };

    const showDeleteUserModal = (user) => {
      modalType.value = 'delete';
      selectedUser.value = user;
      showModal.value = true;
    };

    const addUser = async () => {
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/api/adduser`, {
          name: newUsername.value
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
          users.value.push(data.data);
        }
      } catch (e) {
        alert(e.message);
      } finally {
        closeModal();
      }
    };

    const deleteUser = async () => {
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/api/deluser`, {
          userid: selectedUser.value.userid,
          name: selectedUser.value.username
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
          users.value = users.value.filter(user => user.userid !== selectedUser.value.userid);
        }
      } catch (e) {
        alert(e.message);
      } finally {
        closeModal();
      }
    };

    const permissionText = (permission) => {
      switch (permission) {
        case 0: return '正常';
        case -1: return '封禁';
        case 1: return '管理员';
        default: return '需刷新页面';
      }
    };

    const toggleBan = async (user) => {
      const newPermission = user.permissions === 0 ? -1 : 0;
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/api/setuser`, {
          userid: selectedUser.value.userid,
          name: selectedUser.value.username,
          set_permissions: newPermission
        }, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${import.meta.env.VITE_ADMIN_TOKEN}`
          }
        });
        if (response.data.code === 200) {
          user.permissions = newPermission;
        }
        else{
          alert(data.message);
        }
      } catch (error) {
        console.error('Error toggling user ban:', error);
      } finally {
        closeBanModal();
      }
    };
    const prepareBanUser = (user) => {
      selectedUser.value = user;
      showBanModal.value = true;
      console.log(selectedUser,showBanModal);
    };
    const closeBanModal = ()=> {
      showBanModal.value = false;
      selectedUser.value = null;
    };
    const banActionText= ()=> {
      if (selectedUser.value.permissions == 0) {
        return '封禁';
      } else {
        return '解封';
      }
    };

    const regentoken = async (user) => {
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/api/setuser`, {
          userid: user.userid,
          name: user.username,
          regen_token: true
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
          user.usertoken = data.data.usertoken;
        } else {
          alert(data.message);
        }
      } catch (e) {
        alert(e.message); 
      } finally {
        closeRegenTokenModal();
      }
    };

    const prepareRegenToken = (user) => {
      selectedUser.value = user;
      showRegenTokenModal.value = true;
    };

    const closeRegenTokenModal = () => {
      showRegenTokenModal.value = false;
      selectedUser.value = {};
    };

    const closeModal = () => {
      showBanModal.value = false;
      showModal.value = false;
      newUsername.value = '';
      selectedUser.value = {};
    };

    fetchUsers();

    return {
      users,
      error,
      showModal,
      modalType,
      newUsername,
      selectedUser,
      showAddUserModal,
      showDeleteUserModal,
      addUser,
      deleteUser,
      closeModal,
      permissionText,
      toggleBan,
      prepareBanUser,
      closeBanModal,
      banActionText,
      showBanModal,
      regentoken,
      prepareRegenToken,
      closeRegenTokenModal,
      showRegenTokenModal
    };
  }
};
</script>

<style scoped>
.user-management table {
  width: 100%;
  border-collapse: collapse;
}

.user-management th,
.user-management td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.user-management th {
  background-color: #f2f2f2;
  color: #333;
}

.user-management tr:nth-child(even) {
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
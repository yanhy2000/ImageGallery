<template>
  <div class="user-management">
    <h1>用户管理</h1>
    <table>
      <thead>
        <tr>
          <th>用户ID</th>
          <th>用户名</th>
          <th>权限</th>
          <th>用户令牌</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.userid">
          <td>{{ user.userid }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.permissions }}</td>
          <td>{{ user.usertoken }}</td>
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
    const users = ref([]);
    const error = ref(null);

    

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


    fetchUsers();

    return { users, error };
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

</style>
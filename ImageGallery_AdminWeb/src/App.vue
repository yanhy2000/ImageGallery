<template>
  <div id="app">
    <nav>
      <router-link to="/image" class="btn">图片管理</router-link>
      <router-link to="/user" class="btn">用户管理</router-link>
      <router-link to="/album" class="btn">相册管理</router-link>
    </nav>
    <router-view/>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

.btn {
  display: inline-block;
  margin: 0 10px;
  padding: 10px 20px;
  font-size: 16px;
  text-decoration: none;
  color: #ffffff;
  background-color: #007bff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn:hover {
  background-color: #0056b3;
}
</style>

// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import ImageManagement from '@/views/ImageManagement.vue';
import UserManagement from '@/views/UserManagement.vue';
import AlbumManagement from '@/views/AlbumManagement.vue';

const routes = [
  { path: '/', redirect: '/image' },
  { path: '/image', component: ImageManagement },
  { path: '/user', component: UserManagement },
  { path: '/album', component: AlbumManagement },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

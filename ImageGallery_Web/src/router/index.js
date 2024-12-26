import { createRouter, createWebHistory } from 'vue-router';
import IndexManager from '../views/IndexManager.vue';

const routes = [
  {
    path: '/',
    name: 'IndexManager',
    component: IndexManager
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

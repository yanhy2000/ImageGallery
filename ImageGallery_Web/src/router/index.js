import { createRouter, createWebHistory } from 'vue-router';
import IndexManager from '@/views/IndexManager.vue';
import UploadView from '@/views/UploadView.vue';
import AccountManager from '../views/AccountManager.vue';

const routes = [
  { path: '/', component: IndexManager },
  { path: '/upload', component: UploadView },
  { path: '/account', component: AccountManager },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

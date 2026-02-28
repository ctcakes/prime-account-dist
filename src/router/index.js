import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Create from '../views/Create.vue';
import Link from '../views/Link.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/create',
    name: 'Create',
    component: Create
  },
  {
    path: '/link/:uuid',
    name: 'Link',
    component: Link
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './views/HomePage.vue'; // Home 页面
import AboutPage from './views/AboutPage.vue'; // About 页面

const routes = [
    { path: '/', component: HomePage },
    { path: '/about', component: AboutPage },
];

const router = createRouter({
    history: createWebHistory(), // 使用 HTML5 模式
    routes,
});

export default router;
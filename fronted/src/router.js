// router.js

import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './views/HomePage.vue';
import GoodsPage from "./views/GoodsPage.vue";
import TaskPage from "./views/TaskPage.vue";
import LoginPage from "@/views/LoginPage.vue";


const routes = [
    {name:'home', path: '/home', component: HomePage ,meta: { showSidebar: true,requiresAuth: true},},
    {name:'goods', path: '/goods', component: GoodsPage, meta: { showSidebar: true,requiresAuth: true },},
    {name:'task', path: '/task', component: TaskPage, meta: { showSidebar: true,requiresAuth: true },},
    {name:'login', path: '/login', component: LoginPage, meta: { showSidebar: false,requiresAuth: false }, }, // 404 页面
];


const router = createRouter({
    history: createWebHistory(), // 使用 HTML5 模式
    routes,
});


router.beforeEach((to, from, next) => {
    const isLoggedIn = !!localStorage.getItem('token'); // 检查是否有 token
    if (to.matched.some((record) => record.meta.requiresAuth)) {
        if (!isLoggedIn) {
            next({
                path: '/login', // 跳转到登录页面
                query: { redirect: to.fullPath }, // 保存跳转前的页面，登录后可返回
            });
        } else {
            next();
        }
    } else {
        next(); // 不需要登录的页面，直接访问
    }
});

export default router;
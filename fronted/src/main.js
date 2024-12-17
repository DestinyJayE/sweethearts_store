// main.js

import { createApp } from 'vue';
import App from '@/App.vue';
import router from '@/router'; // 引入路由配置

const app = createApp(App);
app.use(router); // 挂载路由
app.mount('#app');
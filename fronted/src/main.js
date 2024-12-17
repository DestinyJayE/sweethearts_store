// main.js

import { createApp } from 'vue';
import App from '@/App.vue';
import router from '@/router'; // 引入路由配置
import { ElMessage } from 'element-plus';

const app = createApp(App);
app.use(router); // 挂载路由
app.mount('#app');

window.onerror = function (msg, url, line, col, error) {
    // 处理错误信息
    console.error('Error:', msg, 'Script:', url, 'Line:', line, 'Column:', col, 'Error object:', error);
    ElMessage.error('发生未知错误，请稍后重试。');
    // 可以选择发送错误到后端服务器
};

window.addEventListener('unhandledrejection', function (event) {
    console.error('Unhandled rejection (promise):', event.reason);
    ElMessage.error('发生未知错误，请稍后重试。');
    // 可以选择发送错误到后端服务器
    event.preventDefault();
});
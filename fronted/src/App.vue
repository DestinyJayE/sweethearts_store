<!-- App.vue -->
<template>
  <div id="app">
    <!-- 侧边栏 -->
    <SidebarMenu v-if = "showSidebar"/>

    <!-- 动态渲染的页面内容 -->
    <div class="content">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import SidebarMenu from './components/SidebarMenu.vue';

const route = useRoute();

const showSidebar = computed(() => {
  return route.meta?.showSidebar !== false;
});
</script>

<style>
/* 样式可以根据需要自定义 */
#app {
  display: flex;
  height: 100vh;
}

.content {
  flex: 1;
  padding: 20px;
}

.el-message {
  position: fixed !important; /* 固定在屏幕上 */
  top: 20px !important; /* 距离顶部 20px */
  left: 50% !important; /* 水平居中 */
  transform: translateX(-50%) scale(0.5); /* 居中调整 */
  z-index: 9999 !important; /* 确保它在最上层 */
  
}
</style>
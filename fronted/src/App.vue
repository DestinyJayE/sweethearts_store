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
</style>
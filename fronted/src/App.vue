<template>
  <div id="app">
    <!-- 侧边栏 -->
    <SidebarMenu />

    <!-- 动态渲染的页面内容 -->
    <div class="content">
      <router-view />
    </div>
  </div>
</template>

<script>
import SidebarMenu from './components/SidebarMenu.vue';

export default {
  name: 'App',
  components: {
    SidebarMenu,
  },
};
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
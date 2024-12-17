<!-- components/SidebarMenu.vue -->
<template>
  <div class="sidebar">
    <ul>
      <li>
        <router-link to="/home">
          <i class="fas fa-heart"></i> Home
        </router-link>
      </li>
      <li>
        <router-link to="/goods">
          <i class="fas fa-gift"></i> Goods
        </router-link>
      </li>
      <li>
        <router-link to="/task">
          <i class="fas fa-tasks"></i> Task
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'SidebarMenu',
};
</script>

<style scoped>
.sidebar {
  width: 75px;
  background-color: #ffe6f2; /* 淡粉色背景 */
  padding: 20px;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  border-right: 2px solid #ffb3d9; /* 粉色边框 */
}

.sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar ul li {
  margin: 15px 0;
}

.sidebar ul li a {
  text-decoration: none;
  color: #e91e63; /* 深粉色文字 */
  display: flex;
  align-items: center;
  transition: color 0.3s ease;
}

.sidebar ul li a i {
  margin-right: 8px;
  font-size: 1.2em; /* 图标稍微放大 */
}

.sidebar ul li a:hover {
  color: #ff4081; /* 悬停时更亮的粉色 */
}

.sidebar ul li a.router-link-active {
  font-weight: bold;
  color: #ff4081; /* 激活时更亮的粉色 */
}
</style>
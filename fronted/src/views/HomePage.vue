<template>
  <div class="home-list-container">
    <div class="home-list">
      <h1>我购买的商品</h1>
      <div class="user-balance">
        <span>余额：{{ userBalance }} </span>
      </div>
      <table border="1" style="width: 100%; text-align: center;">
        <thead>
        <tr>
          <th>名称</th>
          <th>价格</th>
          <th>描述</th>
          <th>库存</th>
          <th>操作</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="goods in goodsList" :key="goods.id">
          <td>{{ goods.name }}</td>
          <td>{{ goods.price }}</td>
          <td>{{ goods.des }}</td>
          <td>{{ goods.user_purchased_quantity }}</td>
          <td>
            <button @click="confirmUseGoods(goods)">使用</button>
          </td>
        </tr>
        </tbody>
      </table>

      <!-- Modal for confirmation -->
      <div v-if="showModal" class="modal">
        <div class="modal-content">
          <h2>确认使用商品</h2>
          <p>您确定要使用 {{ selectedGoods.name }} 吗？</p>
          <div class="modal-actions">
            <button @click="useGoods(selectedGoods.id)">确认</button>
            <button @click="showModal = false">取消</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import GoodsAPI from "@/api/goods";
import UserAPI from "@/api/user";

let goodsList = ref([]);
let userBalance = ref(0);
let showModal = ref(false);
let selectedGoods = ref({});

function getUserBalance() {
  UserAPI.getPoint().then(res => {
    userBalance.value = res;
  });
}

function getBoughtGoods() {
  GoodsAPI.getBoughtGoods().then(res => {
    goodsList.value = res;
  });
}

function confirmUseGoods(goods) {
  selectedGoods.value = goods;
  showModal.value = true;
}

function useGoods(id) {
  GoodsAPI.useGoods(id).then(() => {
    getBoughtGoods();
    showModal.value = false;
  });
}

onMounted(() => {
  getBoughtGoods();
  getUserBalance();
});
</script>

<style scoped>
.home-list-container{
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: flex-start; /* 顶部对齐 */
  min-height: 100vh; /* 确保至少占据整个视口高度 */
  background-color: #fff5f7;/* 浅粉色背景，营造温馨氛围 */
  padding: 20px;
  border-radius: 10px;
}

.home-list {
  width: 100%;
  font-family: 'Arial', sans-serif;
  background-color: #fff; /* 浅粉色背景 */
  padding: 20px;
  max-width: 1980px;
  margin: 20px auto;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  color: #ff6b81; /* 温暖的粉红色 */
  font-size: 2rem;
  margin-bottom: 20px;
}

.user-balance {
  text-align: right;
  font-size: 1.2rem;
  color: #333;
  margin-bottom: 20px;
}

.user-balance span {
  font-weight: bold;
  color: #ff6b81;
}

button {
  cursor: pointer;
  background-color: #ff6b81;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

button:hover {
  background-color: #ff4757;
}

button:disabled {
  background-color: #f5a5b5;
  cursor: not-allowed;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  background-color: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

thead {
  background-color: #ff6b81;
  color: white;
}

th,
td {
  padding: 10px;
  text-align: center;
  min-width: 100px; /* 单元格最小宽度 */
  max-width: 200px; /* 单元格最大宽度 */
  word-wrap: break-word; /* 允许长单词换行 */
  padding: 10px; /* 单元格内边距 */
  border: 1px solid #f2f2f2;
}

tbody tr:nth-child(odd) {
  background-color: #fdf2f4; /* 浅粉色 */
}

tbody tr:nth-child(even) {
  background-color: #fff;
}

tbody tr:hover {
  background-color: #ffe6eb;
}

/* 模态框样式 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  width: 90%; /* 默认宽度为 90% */
  max-width: 400px; /* 最大宽度为 400px */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  text-align: center;
}

.modal-content h2 {
  color: #ff6b81;
  margin-bottom: 20px;
}

.modal-content label {
  display: block;
  margin: 10px 0;
  text-align: left;
  color: #333;
}

.modal-content input,
.modal-content textarea {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
}

.modal-content textarea {
  resize: none;
  height: 80px;
}

.modal-actions {
  margin-top: 20px;
}

.modal-actions button {
  margin: 0 10px;
}

/* 响应式设计 - 小屏幕优化 */
@media (max-width: 768px) {
  h1 {
    font-size: 1.5rem;
  }

  .home-list {
    padding: 10px;
    margin: 10px;
  }

  .user-balance {
    font-size: 1rem;
  }

  table {
    font-size: 0.9rem;
  }

  th,
  td {
    padding: 5px;
  }

  button {
    padding: 8px 15px;
    font-size: 0.9rem;
  }

  .modal-content {
    width: 95%;
    padding: 15px;
  }
}

/* 响应式设计 - 超小屏幕优化 */
@media (max-width: 480px) {
  h1 {
    font-size: 1.2rem;
  }

  .user-balance {
    font-size: 0.9rem;
    text-align: left; /* 调整余额文字居左 */
  }

  table {
    font-size: 0.8rem;
  }

  button {
    padding: 6px 10px;
    font-size: 0.8rem;
  }

  th,
  td {
    padding: 4px;
  }
}
</style>
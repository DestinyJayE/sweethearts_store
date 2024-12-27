<template>
  <div class="home-list-container">
    <div class="home-list">
      <h1>我购买的商品</h1>
      <div class="user-balance">
        <span>积分：{{ userBalance }}</span>
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
              <div class="table-button-container">
                <div class="button-item">
                <button @click="showDetails(goods)">详情</button>
                </div>
                <div class="button-item">
                <button @click="confirmUseGoods(goods)">使用</button>
              </div>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Modal for "使用" confirmation -->
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

      <!-- Modal for "详情" -->
      <div v-if="showDetailsModal" class="modal">
        <div class="modal-content">
          <h2>商品详情</h2>
          <form>
            <div
              v-for="key in Object.keys(fieldMap)"
              :key="key"
              class="form-group"
            >
              <label :for="fieldMap[key]">{{ fieldMap[key] }}:</label>
              <div class="detail-text">
                <textarea
                  :id="fieldMap[key]"
                  readonly
                  v-model="selectedGoods[key]"
                  class="text-input"
                ></textarea>
              </div>
            </div>
          </form>
          <div class="modal-actions">
            <button @click="showDetailsModal = false">关闭</button>
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
let showModal = ref(false); // 控制 "使用" 模态框的显示
let selectedGoods = ref({}); // 当前选中的商品对象
let showDetailsModal = ref(false); // 控制 "详情" 模态框的显示

const fieldMap = {
  name: "商品名称",
  price: "商品价格",
  des: "商品描述",
  user_purchased_quantity: "购买数量"
};

// 显示商品详情
function showDetails(goods) {
  selectedGoods.value = goods; // 使用 .value 修改 ref 的值
  showDetailsModal.value = true; // 打开详情模态框
}

// 确认使用商品
function confirmUseGoods(goods) {
  selectedGoods.value = goods; // 设置当前选中的商品
  showModal.value = true; // 打开使用模态框
}

// 获取用户余额
function getUserBalance() {
  UserAPI.getPoint().then(res => {
    userBalance.value = res.data;
  });
}

// 获取用户已购买的商品列表
function getBoughtGoods() {
  GoodsAPI.getBoughtGoods().then(res => {
    goodsList.value = res.data;
  });
}



// 使用商品
function useGoods(id) {
  GoodsAPI.useGoods(id).then(() => {
    getBoughtGoods(); // 更新商品列表
    showModal.value = false; // 关闭使用模态框
  });
}

// 页面加载时获取数据
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

.table-button-container {
  display: flex; /* 使用flex布局使子元素水平排列 */
  justify-content: space-around; /* 平均分布子元素 */
}

.button-item {
  /* 每个按钮的容器样式 */
  margin: 0 5px; /* 添加一些外边距 */
}


table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  background-color: white;
  border-radius: 10px;
  overflow: hidden;
  min-height: auto;
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
  overflow: hidden; /* 确保内容不会溢出单元格 */
  white-space: nowrap; /* 防止内容换行 */
  text-overflow: ellipsis; /* 当内容超出时显示省略号 */
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

.text-input{
  max-width: 300px; /* 设置最大宽度 */
  word-wrap: break-word; /* 允许长单词换行 */
  white-space: normal; /* 允许文本换行 */
  overflow-wrap: break-word; /* 允许在长单词或URL内部进行换行 */
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
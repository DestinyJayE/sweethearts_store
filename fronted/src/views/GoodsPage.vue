<template>
  <div class="goods-list-container">
  <div class="goods-list">
    <!-- 右上角余额显示 -->
    <h1>商品列表</h1>
    <div class="user-balance">
      <span>余额：{{ userBalance }} </span>
    </div>
    <div class="button-container">
    <button @click="toggleGoodsView">{{ isMyGoods ? '我发布的商品' : 'TA发布的商品' }}</button>
    <button v-if="isMyGoods" @click="openAddGoodsModal">添加商品</button>
    </div>
    <!-- 我的商品表格 -->
    <table v-if="isMyGoods" border="1" style="width: 100%; text-align: center;">
      <thead>
      <tr>
        <th>ID</th>
        <th>名称</th>
        <th>价格</th>
        <th>描述</th>
        <th>库存</th>
        <th>操作</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="goods in goodsList" :key="goods.id">
        <td>{{ goods.id }}</td>
        <td>{{ goods.name }}</td>
        <td>{{ goods.price }}</td>
        <td>{{ goods.des }}</td>
        <td>{{ goods.num }}</td>
        <td>
          <button @click="deleteGoods(goods.id)">删除</button>
        </td>
      </tr>
      </tbody>
    </table>

    <!-- TA的商品表格 -->
    <table v-else border="1" style="width: 100%; text-align: center;">
      <thead>
      <tr>
        <th>ID</th>
        <th>名称</th>
        <th>价格</th>
        <th>描述</th>
        <th>库存</th>
        <th>操作</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="goods in sweetheartGoodsList" :key="goods.id">
        <td>{{ goods.id }}</td>
        <td>{{ goods.name }}</td>
        <td>{{ goods.price }}</td>
        <td>{{ goods.des }}</td>
        <td>{{ goods.num }}</td>
        <td>
          <button @click="buyGoods(goods.id)" :disabled="goods.num === 0">
            {{ goods.num === 0 ? '已售罄' : '购买' }}
          </button>
        </td>
      </tr>
      </tbody>
    </table>

    <!-- 添加商品模态框 -->
    <div v-if="showAddGoodsModal" class="modal">
      <div class="modal-content">
        <h2>添加商品</h2>
        <label>
          名称：
          <input v-model="newGoods.name" type="text" />
        </label>
        <label>
          价格：
          <input v-model="newGoods.price" type="number" />
        </label>
        <label>
          描述：
          <textarea v-model="newGoods.des"></textarea>
        </label>
        <label>
          库存：
          <input v-model="newGoods.num" type="number" />
        </label>
        <div class="modal-actions">
          <button @click="submitGoods">提交</button>
          <button @click="closeAddGoodsModal">取消</button>
        </div>
      </div>
    </div>

    <!-- 购买反馈模态框 -->
    <div v-if="showFeedbackModal" class="modal">
      <div class="modal-content">
        <h2>{{ feedbackMessage }}</h2>
        <button @click="closeFeedbackModal">确定</button>
      </div>
    </div>
  </div>
  </div>
</template>

<script setup>
import GoodsAPI from "@/api/goods";
import UserAPI from "@/api/user";
import { ref, onMounted } from "vue";

let goodsList = ref([]); // 我的商品列表
let sweetheartGoodsList = ref([]); // TA的商品列表
let isMyGoods = ref(true); // 当前是否展示“我的商品”
let showAddGoodsModal = ref(false); // 控制显示添加商品的模态框
let showFeedbackModal = ref(false); // 控制显示购买反馈的模态框
let feedbackMessage = ref(""); // 购买反馈信息
let userBalance = ref(0); // 用户余额
let newGoods = ref({
  name: "",
  price: 0,
  des: "",
  num: 0
});



// 获取商品数据
function refreshGoodsList() {
  GoodsAPI.getSelfGoods().then(res => {
    goodsList.value = res;
  });
}
function refreshSweetheartGoodsList() {
  GoodsAPI.getSweetheartGoods().then(res => {
    sweetheartGoodsList.value = res;
  });
}

// 获取用户余额
function refreshUserBalance() {
  UserAPI.getPoint().then(res => {
    userBalance.value = res; // 假设接口返回格式为 { data: 余额 }
  });
}

// 切换商品视图
function toggleGoodsView() {
  isMyGoods.value = !isMyGoods.value;
}

// 删除商品
function deleteGoods(id) {
  GoodsAPI.deleteGoods(id).then(() => {
    refreshGoodsList();
    refreshSweetheartGoodsList();
  });
}

// 购买商品
function buyGoods(id) {
  GoodsAPI.buyGoods(id).then(() => {
    feedbackMessage.value = "购买成功！"; // 设置成功反馈信息
    showFeedbackModal.value = true; // 打开反馈模态框
    refreshSweetheartGoodsList(); // 刷新商品列表
    refreshUserBalance(); // 刷新余额
  }).catch(() => {
    feedbackMessage.value = "购买失败，请稍后重试！"; // 设置失败反馈信息
    showFeedbackModal.value = true; // 打开反馈模态框
  });
}

// 打开添加商品模态框
function openAddGoodsModal() {
  showAddGoodsModal.value = true;
}

// 关闭添加商品模态框
function closeAddGoodsModal() {
  showAddGoodsModal.value = false;
  resetNewGoods();
}

// 关闭反馈模态框
function closeFeedbackModal() {
  showFeedbackModal.value = false;
}

// 提交新商品
function submitGoods() {
  GoodsAPI.addGoods(newGoods.value).then(() => {
    refreshGoodsList();
    closeAddGoodsModal();
  });
}

// 重置新商品数据
function resetNewGoods() {
  newGoods.value = {
    name: "",
    price: 0,
    des: "",
    num: 0
  };
}

// 初始化加载商品和用户数据
onMounted(() => {
  refreshGoodsList();
  refreshSweetheartGoodsList();
  refreshUserBalance(); // 加载余额
});
</script>

<style scoped>
/* 整体布局 */
.goods-list-container {
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: flex-start; /* 顶部对齐 */
  min-height: 100vh; /* 确保至少占据整个视口高度 */
  background-color: #fff5f7; /* 浅粉色背景，营造温馨氛围 */
  padding: 20px;
}

/* 商品列表主体 */
.goods-list {
  width: 100%;
  max-width: 1200px; /* 设置最大宽度，防止过宽 */
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  background-color: #fff;
}

h1 {
  text-align: center;
  color: #ff6b81; /* 温暖的粉红色 */
  font-size: 2rem;
  margin-bottom: 20px;
}

/* 用户余额 */
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

.button-container {
  display: flex;
  justify-content: space-between; /* 将按钮分散对齐，左边一个，右边一个 */
  align-items: center; /* 可选：垂直居中对齐 */
}

/* 按钮组 */
button {
  cursor: pointer;
  background-color: #ff6b81; /* 粉红色按钮 */
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px 15px;
  font-size: 1rem;
  margin: 5px;
  transition: all 0.3s ease;
}

button:hover {
  background-color: #ff4757; /* 更深的红色 */
}

button:disabled {
  background-color: #f5a5b5; /* 禁用按钮的浅粉色 */
  cursor: not-allowed;
}

/* 表格样式 */
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  background-color: #fff;
  border-radius: 8px;
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
  border: 1px solid #f2f2f2;
}

tbody tr:nth-child(odd) {
  background-color: #fdf2f4; /* 浅粉色背景 */
}

tbody tr:nth-child(even) {
  background-color: #fff;
}

tbody tr:hover {
  background-color: #ffe6eb; /* 鼠标悬停时的高亮 */
}

/* 添加任务模态框 */
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
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  width: 400px;
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

/* 响应式设计 */
@media (max-width: 768px) {
  .task-list {
    padding: 15px;
  }

  table {
    font-size: 0.9rem;
  }

  modal-content {
    width: 90%;
  }
}
</style>
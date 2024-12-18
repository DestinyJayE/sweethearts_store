<template>
  <div class="task-list-container">
  <div class="task-list">
    <h1>任务列表</h1>
    <div class="user-balance">
      <span>余额：{{ userBalance }} </span>
    </div>
    <div class="button-container">
    <button @click="toggleTaskView">{{ isMyTask ? '我创建的任务' : 'TA创建的任务' }}</button>
    <button v-if="isMyTask" @click="openAddTaskModal">添加任务</button>
    </div>
    <!-- 我的任务表格 -->
    <table v-if="isMyTask" border="1" style="width: 100%; text-align: center;">
      <thead>
      <tr>
        <th>名称</th>
        <th>价格</th>
        <th>描述</th>
        <th>状态</th>
        <th>操作</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="task in tasks" :key="task.id">
        <td>{{ task.name }}</td>
        <td>{{ task.price }}</td>
        <td>{{ task.des }}</td>
        <td>{{ task.is_finish === 0 ? '未完成' : '已完成' }}</td>
        <td>
          <div class="table-button-container">
              <div class="button-item">
                <button @click="deleteTask(task.id)">删除</button>
              </div>
              <div class="button-item">
                <button @click="completeTask(task.id)" :disabled="task.is_finish !== 0">完成</button>
              </div>
          </div>
        </td>
      </tr>
      </tbody>
    </table>

    <!-- TA给我的任务表格 -->
    <table v-else border="1" style="width: 100%; text-align: center;">
      <thead>
      <tr>
        <th>ID</th>
        <th>名称</th>
        <th>价格</th>
        <th>描述</th>
        <th>状态</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="task in sweetheartTasks" :key="task.id">
        <td>{{ task.id }}</td>
        <td>{{ task.name }}</td>
        <td>{{ task.price }}</td>
        <td>{{ task.des }}</td>
        <td>{{ task.is_finish === 0 ? '未完成' : '已完成' }}</td>
      </tr>
      </tbody>
    </table>

    <!-- 添加任务模态框 -->
    <div v-if="showAddTaskModal" class="modal">
      <div class="modal-content">
        <h2>添加任务</h2>
        <label>
          名称：
          <input v-model="newTask.name" type="text" />
        </label>
        <label>
          价格：
          <input v-model="newTask.price" type="number" />
        </label>
        <label>
          描述：
          <textarea v-model="newTask.des"></textarea>
        </label>
        <div class="modal-actions">
          <button @click="submitTask">提交</button>
          <button @click="closeAddTaskModal">取消</button>
        </div>
      </div>
    </div>
  </div>
  </div>
</template>


<script setup>

import TaskAPI from "@/api/task";
import {ref} from "vue";
import {onMounted} from "vue";
import UserAPI from "@/api/user";

let tasks = ref([]); // 我的任务
let sweetheartTasks = ref([]); // TA的任务
let isMyTask = ref(true); // 当前是否展示“我的任务”
let showAddTaskModal = ref(false); // 控制显示添加任务的模态框
let userBalance = ref(0); // 用户余额
let newTask = ref({
  name: "",
  price: 0,
  des: ""
});

// 获取任务数据
function refreshTask() {
  TaskAPI.getSelfTasks().then(res => {
    tasks.value = res;
  });
}
function refreshSweetheartTask() {
  TaskAPI.getSweetheartTask().then(res => {
    sweetheartTasks.value = res;
  });
}

// 切换任务视图
function toggleTaskView() {
  isMyTask.value = !isMyTask.value;
}

// 完成任务
function completeTask(id) {
  TaskAPI.finishTask(id).then(() => {
    refresh()
  });
}

// 删除任务
function deleteTask(id) {
  TaskAPI.deleteTask(id).then(() => {
    refresh()
  });
}

// 打开添加任务模态框
function openAddTaskModal() {
  showAddTaskModal.value = true;
}

// 关闭添加任务模态框
function closeAddTaskModal() {
  showAddTaskModal.value = false;
  resetNewTask();
}

// 提交新任务
function submitTask() {
  TaskAPI.addTask(newTask.value).then(() => {
    refreshTask();
    closeAddTaskModal();
  });
}

function getPoint(){
  UserAPI.getPoint().then((resp)=>{
    userBalance.value = resp;
  })
}

// 重置新任务数据
function resetNewTask() {
  newTask.value = {
    name: "",
    price: 0,
    des: ""
  };
}

function refresh() {
  refreshTask();
  refreshSweetheartTask();
  getPoint();
}

// 初始化加载任务数据
onMounted(() => {
  refreshTask();
  refreshSweetheartTask();
  getPoint();
});
</script>

<style scoped>

.task-list-container {
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: flex-start; /* 顶部对齐 */
  min-height: 100vh; /* 确保至少占据整个视口高度 */
  background-color: #fff5f7; /* 浅粉色背景，营造温馨氛围 */
  padding: 20px;
}
/* 页面整体样式 */
.task-list {
  font-family: 'Arial', sans-serif;
  background-color: #fff; /* 浅粉色背景 */
  padding: 20px;
  max-width: 900px;
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

.user-balance span{
  font-weight: bold;
  color: #ff6b81;
}

.button-container {
  display: flex;
  justify-content: space-between; /* 将按钮分散对齐，左边一个，右边一个 */
  align-items: center; /* 可选：垂直居中对齐 */
}

.table-button-container {
  display: flex; /* 使用flex布局使子元素水平排列 */
  justify-content: space-around; /* 平均分布子元素 */
}

.button-item {
  /* 每个按钮的容器样式 */
  margin: 0 5px; /* 添加一些外边距 */
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

  .modal-content {
    width: 90%;
  }
}
</style>
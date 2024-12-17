<!-- views/LoginPage.vue -->
<template>
  <div class="login-container">
    <h1>欢迎回来</h1>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="username">用户名:</label>
        <input
            type="text"
            id="username"
            v-model="LoginData.user_name"
            required
            placeholder="请输入用户名"
        />
      </div>
      <div class="form-group">
        <label for="password">密码:</label>
        <input
            type="password"
            id="password"
            v-model="LoginData.password"
            required
            placeholder="请输入密码"
        />
      </div>
      <div class="form-group">
        <button type="submit">登录</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import router from '@/router';
import UserAPI from '@/api/user';

const LoginData = ref({ user_name: "", password: "" });

async function handleLogin() {
  const params = { ...LoginData.value };
  UserAPI
      .login(params)
      .then((response) => {
        const { token } = response;
        localStorage.setItem('token', token);
        localStorage.setItem('user_name', LoginData.value.user_name);
        router.push({ path: "/home", params: { user_name: LoginData.value.user_name } });
      })
      .catch(error => {
        console.error("登录失败:", error);
        // 可以添加错误提示逻辑
      });
}
</script>

<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #fff5f7; /* 浅粉色背景 */
  padding: 20px;
}

h1 {
  color: #ff6b81; /* 粉色标题 */
  margin-bottom: 30px;
  font-size: 2.5rem;
  text-align: center;
}

form {
  width: 100%;
  max-width: 400px;
  background-color: #fff;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: bold;
}

input[type="text"],
input[type="password"] {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
  margin-top: 5px;
  box-sizing: border-box; /* 保证内边距不影响宽度 */
}

input::placeholder {
  color: #aaa;
}

button {
  cursor: pointer;
  background-color: #ff6b81; /* 粉色按钮 */
  color: white;
  border: none;
  border-radius: 5px;
  padding: 12px 20px;
  font-size: 1.1rem;
  transition: background-color 0.3s ease;
  width: 100%;
}

button:hover {
  background-color: #ff4757; /* 深粉色按钮 */
}

/* 响应式设计 */
@media (max-width: 768px) {
  form {
    padding: 20px;
  }

  h1 {
    font-size: 2rem;
  }
}
</style>
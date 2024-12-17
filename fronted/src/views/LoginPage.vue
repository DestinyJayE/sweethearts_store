<!-- views/LoginPage.vue -->
<template>
    <div class="login-container">
      <h1>Login Page</h1>
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="username">Username:</label>
          <input type="text" id="username" v-model="username" required>
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <input type="password" id="password" v-model="password" required>
        </div>
        <div class="form-group">
          <button @click='submitForm' type="submit">Login</button>
        </div>
      </form>
    </div>
</template>
  
<script>
import { UserAPI } from '@/api/user'
export default 
{
    name: 'LoginPage',
    data() {
      return {
        username: '',
        password: ''
      };
    },
    methods: 
    {
        submitForm() 
        {
            try 
            {
                const response = UserAPI.login({
                username: this.username,
                password: this.password
                });
                // 处理响应，例如保存token，跳转到主页等
                console.log(response);
                // 假设响应中包含token
                if (response.token) 
                    {
                        // 保存token到localStorage或Vuex
                        localStorage.setItem('token', response.token);
                        // 跳转到主页或其他页面
                        this.$router.push({ name: 'home' });
                    }
            } catch (error) 
            {
                // 处理错误，例如显示错误消息
                console.error(error);
            }
        }
    }
}
</script>
  
 <style scoped>
 .login-container {
    max-width: 300px;
    margin: 50px auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
  }
  
  input[type="text"],
  input[type="password"] {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  button {
    width: 100%;
    padding: 10px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  </style>
  
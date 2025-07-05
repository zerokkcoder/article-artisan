<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <h2>用户登录</h2>
        </div>
      </template>
      
      <el-form
          ref="loginFormRef"
          :model="loginForm"
          :rules="rules as any"
          class="login-form"
          label-position="top"
        >
          <el-form-item label="用户名" prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            prefix-icon="User"
            clearable
          />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="Lock"
            show-password
            clearable
          />
        </el-form-item>
        
        <el-form-item class="button-group" label-width="0">
          <el-button
            type="primary"
            :loading="isLoading"
            @click="handleLogin"
            class="login-button"
          >
            登录
          </el-button>
          <el-button @click="switchToRegister" class="switch-button">
            注册账号
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuth } from '../composables/useAuth'
import type { FormInstance } from 'element-plus'

const { login, switchToRegister, isLoading } = useAuth()

const loginFormRef = ref<FormInstance>()
const loginForm = ref({
  username: '',
  password: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  const valid = await loginFormRef.value.validate().catch(() => false)
  if (!valid) return
  
  await login(loginForm.value.username, loginForm.value.password)
}
</script>

<style scoped>
.login-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
  box-sizing: border-box;
}

.login-card {
  width: 100%;
  max-width: 400px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.95);
}

.card-header {
  text-align: center;
}

.card-header h2 {
  margin: 0;
  color: #303133;
  font-weight: 600;
  font-size: 24px;
}

.login-form {
  padding: 20px 0;
}

.button-group {
  text-align: center;
  margin-top: 20px;
}

.button-group :deep(.el-form-item__content) {
  justify-content: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  gap: 12px;
}

.button-group :deep(.el-button) {
  margin: 0 !important;
}

.login-button {
  width: 100%;
  height: 44px;
  font-size: 16px;
}

.switch-button {
  width: 100%;
  height: 44px;
  font-size: 16px;
}

/* 响应式设计 */
@media (max-width: 480px) {
  .login-container {
    padding: 10px;
  }
  
  .login-card {
    max-width: 100%;
  }
  
  .card-header h2 {
    font-size: 20px;
  }
}
</style>
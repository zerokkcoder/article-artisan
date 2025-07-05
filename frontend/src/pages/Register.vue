<template>
  <div class="register-container">
    <el-card class="register-card">
      <template #header>
        <div class="card-header">
          <h2>用户注册</h2>
        </div>
      </template>
      
      <el-form
          ref="registerFormRef"
          :model="registerForm"
          :rules="rules as any"
          class="register-form"
          label-position="top"
        >
          <el-form-item label="用户名" prop="username">
          <el-input
            v-model="registerForm.username"
            placeholder="请输入用户名"
            prefix-icon="User"
            clearable
          />
        </el-form-item>
        
        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="registerForm.email"
            placeholder="请输入邮箱"
            prefix-icon="Message"
            clearable
          />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="registerForm.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="Lock"
            show-password
            clearable
          />
        </el-form-item>
        
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="registerForm.confirmPassword"
            type="password"
            placeholder="请再次输入密码"
            prefix-icon="Lock"
            show-password
            clearable
          />
        </el-form-item>
        
        <el-form-item class="button-group" label-width="0">
          <el-button
            type="primary"
            :loading="isLoading"
            @click="handleRegister"
            class="register-button"
          >
            注册
          </el-button>
          <el-button @click="switchToLogin" class="switch-button">
            已有账号，去登录
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

const { register, switchToLogin, isLoading } = useAuth()

const registerFormRef = ref<FormInstance>()
const registerForm = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (_rule: any, value: any, callback: any) => {
        if (value !== registerForm.value.password) {
          callback(new Error('两次输入密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

const handleRegister = async () => {
  if (!registerFormRef.value) return
  
  const valid = await registerFormRef.value.validate().catch(() => false)
  if (!valid) return
  
  await register(
    registerForm.value.username,
    registerForm.value.email,
    registerForm.value.password,
    registerForm.value.confirmPassword
  )
}
</script>

<style scoped>
.register-container {
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

.register-card {
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

.register-form {
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

.register-button {
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
  .register-container {
    padding: 10px;
  }
  
  .register-card {
    max-width: 100%;
  }
  
  .card-header h2 {
    font-size: 20px;
  }
}
</style>
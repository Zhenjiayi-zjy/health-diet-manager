<template>
  <div class="register-page">
    <h2>用户注册</h2>
    <el-form ref="registerFormRef" :model="registerForm" :rules="registerRules" label-width="80px">
      <el-form-item label="账号" prop="username">
        <el-input v-model="registerForm.username" placeholder="请输入账号"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input v-model="registerForm.password" type="password" placeholder="请输入密码"></el-input>
      </el-form-item>
      <el-form-item label="确认密码" prop="confirmPassword">
        <el-input v-model="registerForm.confirmPassword" type="password" placeholder="请再次输入密码"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleRegister">注册</el-button>
        <span>已有账号？<router-link to="/login">去登录</router-link></span>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import request from '@/utils/request'

const router = useRouter()
const registerFormRef = ref(null)

const registerForm = ref({
  username: '',
  password: '',
  confirmPassword: ''
})

// 两次密码一致性校验
const validateConfirmPassword = (rule, value, callback) => {
  if (value !== registerForm.value.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const registerRules = {
  username: [
    { required: true, message: '请输入账号', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

// 注册处理
const handleRegister = async () => {
  try {
    const valid = await registerFormRef.value.validate()
    if (valid) {
      await request.post('/register', {
        username: registerForm.value.username,
        password: registerForm.value.password
      })
      ElMessage.success('注册成功，请登录')
      router.push('/login')
    }
  } catch (err) {
    console.error('注册失败:', err)
  }
}
</script>

<style scoped>
.register-page {
  width: 400px;
  margin: 80px auto;
  padding: 30px 24px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.06);
}

.register-page h2 {
  text-align: center;
  margin: 0 0 24px 0;
  color: #303133;
  font-weight: 500;
}

.register-page .el-form-item:last-child {
  margin-bottom: 0;
  text-align: center;
}

.register-page span {
  margin-left: 12px;
  font-size: 14px;
  color: #606266;
}
</style>

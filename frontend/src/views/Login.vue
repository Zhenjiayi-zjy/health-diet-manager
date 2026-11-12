<template>
  <div class="login-page">
    <h1>登录页</h1>
    <el-form
      ref="loginFormRef"
      :model="loginForm"
      :rules="loginRules"
      label-width="80px"
      class="login-form"
    >
      <el-form-item label="账号" prop="username">
        <el-input v-model="loginForm.username" placeholder="请输入账号"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input v-model="loginForm.password" type="password" placeholder="请输入密码"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleLogin">登录</el-button>
        <el-button @click="goRegister">去注册</el-button>
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
const loginFormRef = ref(null)

// 表单数据
const loginForm = ref({
  username: '',
  password: ''
})

// 表单校验规则
const loginRules = {
  username: [
    { required: true, message: '请输入账号', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ]
}

// 登录处理
const handleLogin = async () => {
  try {
    const valid = await loginFormRef.value.validate()
    if (valid) {
      const res = await request.post('/api/login', loginForm.value)
      // 存储Token与用户信息
      localStorage.setItem('token', res.data.token)
      localStorage.setItem('userInfo', JSON.stringify(res.data.user))
      ElMessage.success('登录成功')
      router.push('/')
    }
  } catch (err) {
    console.error('登录失败', err)
    ElMessage.error('登录失败，请检查账号密码')
  }
}

// 跳转注册页
const goRegister = () => {
  router.push('/register')
}
</script>

<style scoped>
.login-page {
  width: 400px;
  margin: 120px auto 0;
  padding: 20px;
}

.login-form {
  margin-top: 30px;
}
</style>

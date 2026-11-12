<template>
  <div class="login-page">
    <h1>登录页</h1>
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
    console.error('登录失败:', err)
  }
}
</script>

<style scoped>
.home-page {
  padding: 20px;
  padding-bottom: 60px;
}
</style>

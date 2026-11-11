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

const router = useRouter()
const registerFormRef = ref(null)

// 表单数据
const registerForm = ref({
  username: '',
  password: '',
  confirmPassword: ''
})

// 自定义校验：两次密码一致性校验
const validateConfirmPassword = (rule, value, callback) => {
  if (value !== registerForm.value.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

// 表单校验规则
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
const handleRegister = () => {
  registerFormRef.value.validate((valid) => {
    if (valid) {
      // 模拟注册成功，后续对接后端接口替换此处逻辑
      ElMessage.success('注册成功，请登录')
      router.push('/login')
    }
  })
}
</script>

<style scoped>
</style>

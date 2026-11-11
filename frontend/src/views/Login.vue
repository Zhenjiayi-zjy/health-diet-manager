<template>
  <div class="login-page">
    <h2>用户登录</h2>
    <el-form ref="loginFormRef" :model="loginForm" :rules="loginRules" label-width="80px">
      <el-form-item label="账号" prop="username">
        <el-input v-model="loginForm.username" placeholder="请输入账号"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input v-model="loginForm.password" type="password" placeholder="请输入密码"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleLogin">登录</el-button>
        <span>没有账号？<router-link to="/register">去注册</router-link></span>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

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
const handleLogin = () => {
  loginFormRef.value.validate((valid) => {
    if (valid) {
      // 模拟登录成功，后续对接后端接口替换此处逻辑
      ElMessage.success('登录成功')
      router.push('/')
    }
  })
}
</script>

<style scoped>
.login-page {
  width: 400px;
  margin: 80px auto;
  padding: 30px 24px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.06);
}

.login-page h2 {
  text-align: center;
  margin: 0 0 24px 0;
  color: #303133;
  font-weight: 500;
}

.login-page .el-form-item:last-child {
  margin-bottom: 0;
  text-align: center;
}

.login-page span {
  margin-left: 12px;
  font-size: 14px;
  color: #606266;
}
</style>


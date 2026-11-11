<template>
  <div class="login-page">
    <h2>用户登录</h2>
    <el-form label-width="80px">
      <el-form-item label="账号">
        <el-input placeholder="请输入账号"></el-input>
      </el-form-item>
      <el-form-item label="密码">
        <el-input type="password" placeholder="请输入密码"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary">登录</el-button>
        <span>没有账号？<router-link to="/register">去注册</router-link></span>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
</script>

<style scoped>
</style>

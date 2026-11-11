<template>
  <div class="register-page">
    <h2>用户注册</h2>
    <el-form label-width="80px">
      <el-form-item label="账号">
        <el-input placeholder="请输入账号"></el-input>
      </el-form-item>
      <el-form-item label="密码">
        <el-input type="password" placeholder="请输入密码"></el-input>
      </el-form-item>
      <el-form-item label="确认密码">
        <el-input type="password" placeholder="请再次输入密码"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary">注册</el-button>
        <span>已有账号？<router-link to="/login">去登录</router-link></span>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
</script>

<style scoped>
</style>

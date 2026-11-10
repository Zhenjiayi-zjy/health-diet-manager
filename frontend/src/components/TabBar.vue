<template>
  <div class="tab-bar">
    <router-link to="/" class="tab-item">首页</router-link>
    <router-link to="/diet" class="tab-item">记录</router-link>
    <router-link to="/profile" class="tab-item">我的</router-link>
  </div>
</template>

<script setup>
</script>

<style scoped>
.tab-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 50px;
  display: flex;
  background: #fff;
  border-top: 1px solid #eee;
}
.tab-item {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
  text-decoration: none;
  font-size: 14px;
}
/* 当前选中的页面高亮 */
.tab-item.router-link-active {
  color: #409eff;
  font-weight: 500;
}
</style>

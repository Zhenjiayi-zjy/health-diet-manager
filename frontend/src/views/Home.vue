<template>
  <div class="home-page">
    <h1>首页</h1>
    <!-- 底部导航 -->
    <TabBar />
  </div>
</template>

<script setup>
import TabBar from '../components/TabBar.vue'
</script>

<style scoped>
.home-page {
  padding: 20px;
  padding-bottom: 60px;
}
</style>

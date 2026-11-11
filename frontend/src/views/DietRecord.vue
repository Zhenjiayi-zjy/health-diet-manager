<template>
  <div class="diet-record-page">
    <!-- 顶部日期切换 -->
    <div class="date-bar">
      <el-date-picker
        v-model="currentDate"
        type="date"
        placeholder="选择日期"
        format="YYYY-MM-DD"
        value-format="YYYY-MM-DD"
      />
      <span class="date-tip">查看当日饮食记录</span>
    </div>

    <!-- 饮食录入表单 -->
    <div class="record-form-card">
      <h3>新增饮食记录</h3>
      <el-form ref="formRef" label-width="80px">
        <el-form-item label="食物选择" prop="foodId">
          <el-select v-model="form.foodId" placeholder="请选择食物">
            <el-option label="米饭" value="rice"></el-option>
            <el-option label="鸡蛋" value="egg"></el-option>
            <el-option label="牛奶" value="milk"></el-option>
            <el-option label="苹果" value="apple"></el-option>
            <el-option label="面条" value="noodle"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="食用分量" prop="weight">
          <el-input v-model="form.weight" placeholder="请输入分量（克）"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleAdd">添加记录</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 记录列表 -->
    <div class="record-list">
      <h3>当日记录</h3>
      <el-empty v-if="recordList.length === 0" description="暂无当日饮食记录"></el-empty>
      <div v-else class="list-container">
        <el-card v-for="item in recordList" :key="item.id" class="record-item">
          <div class="item-header">
            <span class="food-name">{{ item.foodName }}</span>
            <el-button type="danger" size="small" @click="handleDelete(item.id)">删除</el-button>
          </div>
          <div class="item-info">
            <span>分量：{{ item.weight }} 克</span>
            <span>热量：{{ item.calorie }} 千卡</span>
            <span>录入时间：{{ item.time }}</span>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const formRef = ref(null)
const currentDate = ref(new Date().toISOString().slice(0, 10))

const form = ref({
  foodId: '',
  weight: ''
})

const recordList = ref([])

// 添加记录
const handleAdd = () => {}

// 删除记录
const handleDelete = (id) => {}
</script>

<style scoped>
</style>

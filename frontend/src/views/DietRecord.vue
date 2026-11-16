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
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
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
          <el-input v-model.number="form.weight" placeholder="请输入分量（克）"></el-input>
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
import { ref, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const formRef = ref(null)
const currentDate = ref(new Date().toISOString().slice(0, 10))

// 食物热量映射表（模拟数据，后续对接后端接口替换）
const foodCalorieMap = {
  rice: { name: '米饭', calorie: 116 },
  egg: { name: '鸡蛋', calorie: 143 },
  milk: { name: '牛奶', calorie: 54 },
  apple: { name: '苹果', calorie: 52 },
  noodle: { name: '面条', calorie: 109 }
}

const form = ref({
  foodId: '',
  weight: ''
})

// 全量记录数据（模拟数据库）
const allRecords = ref([])

// 根据日期筛选的当日记录
const recordList = computed(() => {
  return allRecords.value.filter(item => item.date === currentDate.value)
})

// 表单校验规则
const rules = ref({
  foodId: [{ required: true, message: '请选择食物', trigger: 'change' }],
  weight: [
    { required: true, message: '请输入分量', trigger: 'blur' },
    { type: 'number', message: '请输入数字', trigger: 'blur' }
  ]
})


// 添加记录
const handleAdd = () => {
  formRef.value.validate((valid) => {
    if (valid) {
      const foodInfo = foodCalorieMap[form.value.foodId]
      const totalCalorie = Math.round((foodInfo.calorie * form.value.weight) / 100)
      
      const newRecord = {
        id: Date.now(),
        date: currentDate.value,
        foodId: form.value.foodId,
        foodName: foodInfo.name,
        weight: form.value.weight,
        calorie: totalCalorie,
        time: new Date().toLocaleTimeString()
      }
      
      allRecords.value.unshift(newRecord)
      ElMessage.success('记录添加成功')
      formRef.value.resetFields()
    }
  })
}

// 删除记录
const handleDelete = (id) => {
  ElMessageBox.confirm('确定要删除这条记录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    allRecords.value = allRecords.value.filter(item => item.id !== id)
    ElMessage.success('删除成功')
  }).catch(() => {})
}
</script>

<style scoped>
.diet-record-page {
  padding: 20px;
  padding-bottom: 70px;
  max-width: 600px;
  margin: 0 auto;
}

.date-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.date-tip {
  font-size: 14px;
  color: #666;
}

.record-form-card {
  padding: 20px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  background: #fff;
  margin-bottom: 24px;
}

.record-form-card h3,
.record-list h3 {
  margin: 0 0 16px 0;
  font-size: 16px;
  color: #303133;
}

.record-item {
  margin-bottom: 12px;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.food-name {
  font-size: 15px;
  font-weight: 500;
  color: #303133;
}

.item-info {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  font-size: 13px;
  color: #606266;
}
</style>


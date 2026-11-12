<template>
  <div class="diet-page">
    <h1>饮食记录</h1>
    <TabBar />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/utils/request'

const formRef = ref(null)
const currentDate = ref(new Date().toISOString().slice(0, 10))

// 表单数据
const form = ref({
  foodId: '',
  weight: ''
})

// 记录列表
const recordList = ref([])

// 食物选项列表
const foodOptions = ref([])

// 表单校验规则
const rules = {
  foodId: [{ required: true, message: '请选择食物', trigger: 'change' }],
  weight: [
    { required: true, message: '请输入分量', trigger: 'blur' },
    { type: 'number', message: '请输入数字', trigger: 'blur' }
  ]
}

// 获取食物列表（搜索/初始化）
const getFoodList = async (keyword = '') => {
  try {
    const res = await request.get('/food/search', {
      params: { keyword }
    })
    foodOptions.value = res.data.map(item => ({
      label: item.name,
      value: item.id
    }))
  } catch (err) {
    console.error('获取食物列表失败:', err)
  }
}

// 获取当日饮食记录
const getRecordList = async () => {
  try {
    const res = await request.get('/diet/list', {
      params: { date: currentDate.value }
    })
    recordList.value = res.data
  } catch (err) {
    console.error('获取记录失败:', err)
  }
}

// 添加记录
const handleAdd = async () => {
  try {
    const valid = await formRef.value.validate()
    if (valid) {
      await request.post('/diet/add', {
        foodId: form.value.foodId,
        amount: form.value.weight,
        date: currentDate.value
      })
      ElMessage.success('记录添加成功')
      formRef.value.resetFields()
      // 重新拉取列表
      getRecordList()
    }
  } catch (err) {
    console.error('添加记录失败:', err)
  }
}

// 删除记录
const handleDelete = (id) => {
  ElMessageBox.confirm('确定要删除这条记录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await request.delete(`/diet/${id}`)
      ElMessage.success('删除成功')
      getRecordList()
    } catch (err) {
      console.error('删除失败:', err)
    }
  }).catch(() => {})
}

// 切换日期重新加载数据
const handleDateChange = () => {
  getRecordList()
}

// 页面初始化加载数据
onMounted(() => {
  getFoodList()
  getRecordList()
})

</script>

<style scoped>
.home-page {
  padding: 20px;
  padding-bottom: 60px;
}
</style>

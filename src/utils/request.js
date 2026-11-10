import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建请求实例
const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL, // 从环境变量取接口前缀
  timeout: 10000 // 超时时间10秒
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 后面加token可以写在这里
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    ElMessage.error(error.message || '网络请求失败')
    return Promise.reject(error)
  }
)

export default service

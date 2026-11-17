import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

// 创建axios实例
const service = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// 请求拦截器：自动携带Token
service.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器：统一处理错误与返回
service.interceptors.response.use(
  (response) => {
    const res = response.data
    // 业务成功直接返回数据
    if (res.code === 200 || res.code === 0) {
      return res
    }
    // 业务错误提示
    ElMessage.error(res.message || '请求失败')
    return Promise.reject(new Error(res.message || '请求失败'))
  },
  (error) => {
    // 401未授权：清除Token跳登录页
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      ElMessage.warning('登录已过期，请重新登录')
      router.push('/login')
    } else {
      ElMessage.error(error.message || '网络异常')
    }
    return Promise.reject(error)
  }
)

export default service

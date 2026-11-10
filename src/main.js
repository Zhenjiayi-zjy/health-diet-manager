import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'// 引入路由

// 引入 Element Plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App)
app.use(router)// 使用路由
app.use(ElementPlus) // 使用组件库
app.mount('#app')

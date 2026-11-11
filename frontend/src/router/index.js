import { createRouter, createWebHashHistory } from 'vue-router'

// 导入页面
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Home from '../views/Home.vue'
import DietRecord from '../views/DietRecord.vue'
import Profile from '../views/Profile.vue'


const routes = [
  { path: '/login', component: Login, name: 'login' },
  { path: '/', component: Home, name: 'home' },
  { path: '/diet', component: DietRecord, name: 'diet' },
  { path: '/profile', component: Profile, name: 'profile' }
{ path: '/register', component: Register, name: 'register' },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'

// 创建 Pinia 存储
const store = createPinia()

// 创建 Vue 应用并挂载 Pinia 和 Router
console.log('正在初始化 Vue 应用...')
const app = createApp(App)
app.use(store)
app.use(router)
app.mount('#app')
console.log('Vue 应用初始化完成')
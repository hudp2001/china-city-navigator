import { createRouter, createWebHistory } from 'vue-router'
import ChinaLayout from '../components/ChinaLayout.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: ChinaLayout
    }
  ]
})

export default router
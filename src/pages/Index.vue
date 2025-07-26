<template>
  <div class="provinces-container">
    <h1 class="page-title">中国省份</h1>
    
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>
    
    <div v-else-if="error" class="error-container">
      <p>{{ error }}</p>
      <button @click="loadProvinces" class="retry-button">重试</button>
    </div>
    
    <div class="layout-container">
      <div class="tree-view">
        <h3>省份列表</h3>
        <ul>
          <li v-for="province in provinces" :key="province.id">
            <span @click="toggleProvince(province.id)">{{ province.name }}</span>
            <ul v-if="expandedProvinces.includes(province.id)">
              <li v-for="city in getCitiesByProvince(province.id)" :key="city.id">
                {{ city.name }}
              </li>
            </ul>
          </li>
        </ul>
      </div>
      
      <div class="content-view">
        <div v-if="selectedProvince" class="province-detail">
          <h2>{{ selectedProvince.name }}</h2>
          <p>省会：{{ selectedProvince.capital }}</p>
          <p>人口：{{ formatNumber(selectedProvince.population) }}人</p>
          <p>面积：{{ formatNumber(selectedProvince.area) }}平方公里</p>
          <p>GDP：{{ formatNumber(selectedProvince.gdp) }}亿元</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { loadAllProvinces } from '../services/data-loader'

export default {
  name: 'IndexPage',
  setup() {
    const provinces = ref([])
    const loading = ref(true)
    const error = ref(null)
    const selectedProvince = ref(null)
    const expandedProvinces = ref([])

    const loadProvinces = async () => {
      loading.value = true
      error.value = null
      
      try {
        const data = await loadAllProvinces()
        provinces.value = data
      } catch (err) {
        console.error('Failed to load provinces:', err)
        error.value = '加载省份数据失败，请稍后重试'
      } finally {
        loading.value = false
      }
    }

    const formatNumber = (num) => {
      return num ? num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',') : '0'
    }

    onMounted(() => {
      loadProvinces()
    })

    const getCitiesByProvince = (provinceId) => {
      return provinces.value.find(p => p.id === provinceId)?.cities || []
    }

    const toggleProvince = (provinceId) => {
      if (expandedProvinces.value.includes(provinceId)) {
        expandedProvinces.value = expandedProvinces.value.filter(id => id !== provinceId)
      } else {
        expandedProvinces.value.push(provinceId)
      }
    }

    return {
      provinces,
      loading,
      error,
      loadProvinces,
      formatNumber,
      selectedProvince,
      expandedProvinces,
      getCitiesByProvince,
      toggleProvince
    }
  }
}
</script>

<style scoped>
.provinces-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-title {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
  font-size: 2rem;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
}

.loading-spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top: 4px solid #3498db;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-container {
  text-align: center;
  padding: 30px;
  background-color: #fff3f3;
  border-radius: 8px;
  margin: 20px 0;
}

.retry-button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
  font-size: 1rem;
}

.retry-button:hover {
  background-color: #2980b9;
}

.provinces-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.province-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  text-decoration: none;
  color: inherit;
  height: 100%;
}

.province-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.province-card-content {
  padding: 20px;
}

.province-card h2 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #333;
  font-size: 1.5rem;
}

.province-capital {
  color: #555;
  font-weight: 500;
  margin-bottom: 10px;
}

.province-info {
  color: #666;
  margin: 5px 0;
  font-size: 0.9rem;
}
</style>
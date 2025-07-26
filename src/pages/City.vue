<template>
  <div class="city-container">
    <div class="breadcrumb">
      <router-link to="/" class="breadcrumb-link">首页</router-link>
      <span class="breadcrumb-separator">/</span>
      <router-link :to="`/province/${provinceId}`" class="breadcrumb-link">{{ provinceName }}</router-link>
      <span class="breadcrumb-separator">/</span>
      <span>{{ city?.name || '城市详情' }}</span>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>
    
    <div v-else-if="error" class="error-container">
      <p>{{ error }}</p>
      <button @click="loadData" class="retry-button">重试</button>
      <router-link :to="`/province/${provinceId}`" class="back-button">返回省份页面</router-link>
    </div>
    
    <div v-else-if="city" class="city-detail">
      <div class="city-header">
        <h1>{{ city.name }}</h1>
        <p class="city-description">{{ city.description }}</p>
      </div>
      
      <div class="city-stats">
        <div class="stat-card">
          <div class="stat-value">{{ formatNumber(city.population) }}</div>
          <div class="stat-label">人口 (人)</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ formatNumber(city.area) }}</div>
          <div class="stat-label">面积 (平方公里)</div>
        </div>
      </div>
      
      <div class="city-image-section">
        <div class="city-image-placeholder">
          <span>{{ city.name }}</span>
        </div>
      </div>
      
      <h2 class="attractions-title">著名景点</h2>
      
      <div v-if="!city.attractions || city.attractions.length === 0" class="no-attractions">
        <p>暂无景点数据</p>
      </div>
      
      <div v-else class="attractions-grid">
        <div 
          v-for="(attraction, index) in city.attractions" 
          :key="index" 
          class="attraction-card"
        >
          <div class="attraction-image-container">
            <div class="attraction-image-placeholder">{{ attraction.substring(0, 1) }}</div>
          </div>
          <div class="attraction-card-content">
            <h3>{{ attraction }}</h3>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else class="not-found">
      <h2>未找到城市信息</h2>
      <router-link :to="`/province/${provinceId}`" class="back-button">返回省份页面</router-link>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { loadProvinceData, loadCityData } from '../services/data-loader'

export default {
  name: 'CityPage',
  setup() {
    const route = useRoute()
    const provinceId = ref(route.params.provinceId)
    const cityId = ref(route.params.cityId)
    const provinceName = ref('')
    const city = ref(null)
    const loading = ref(true)
    const error = ref(null)

    const loadData = async () => {
      loading.value = true
      error.value = null
      
      try {
        // 加载省份数据以获取省份名称
        const provinceData = await loadProvinceData(provinceId.value)
        if (provinceData) {
          provinceName.value = provinceData.name
        } else {
          provinceName.value = provinceId.value
        }
        
        // 加载城市数据
        const cityData = await loadCityData(provinceId.value, cityId.value)
        city.value = cityData
        
        if (!cityData) {
          error.value = '未找到该城市的数据'
        }
      } catch (err) {
        console.error('Failed to load city data:', err)
        error.value = '加载数据失败，请稍后重试'
      } finally {
        loading.value = false
      }
    }

    const formatNumber = (num) => {
      return num ? num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',') : '0'
    }

    onMounted(() => {
      loadData()
    })

    // 当路由参数变化时重新加载数据
    watch(
      () => [route.params.provinceId, route.params.cityId],
      ([newProvinceId, newCityId]) => {
        provinceId.value = newProvinceId
        cityId.value = newCityId
        loadData()
      }
    )

    return {
      provinceId,
      cityId,
      provinceName,
      city,
      loading,
      error,
      loadData,
      formatNumber
    }
  }
}
</script>

<style scoped>
.city-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.breadcrumb {
  margin-bottom: 20px;
  font-size: 0.9rem;
  color: #666;
}

.breadcrumb-link {
  color: #3498db;
  text-decoration: none;
}

.breadcrumb-link:hover {
  text-decoration: underline;
}

.breadcrumb-separator {
  margin: 0 8px;
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

.retry-button, .back-button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  margin: 10px 5px;
  font-size: 1rem;
  display: inline-block;
  text-decoration: none;
}

.back-button {
  background-color: #7f8c8d;
}

.retry-button:hover {
  background-color: #2980b9;
}

.back-button:hover {
  background-color: #6c7a7a;
}

.city-header {
  margin-bottom: 30px;
}

.city-header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
  color: #333;
}

.city-description {
  font-size: 1.1rem;
  color: #555;
  line-height: 1.6;
}

.city-stats {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  text-align: center;
}

.stat-value {
  font-size: 1.8rem;
  font-weight: bold;
  color: #3498db;
  margin-bottom: 5px;
}

.stat-label {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.city-image-section {
  margin-bottom: 40px;
}

.city-image-placeholder {
  height: 300px;
  background-color: #3498db;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 2rem;
  font-weight: bold;
}

.attractions-title {
  font-size: 1.8rem;
  margin-bottom: 20px;
  color: #333;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 10px;
}

.no-attractions {
  text-align: center;
  padding: 30px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.attractions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.attraction-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.attraction-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.attraction-image-container {
  height: 150px;
  background-color: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.attraction-image-placeholder {
  font-size: 2rem;
  color: white;
  background-color: #3498db;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.attraction-card-content {
  padding: 15px;
}

.attraction-card h3 {
  margin: 0;
  color: #333;
  font-size: 1.2rem;
  text-align: center;
}

.not-found {
  text-align: center;
  padding: 50px 20px;
}

.not-found h2 {
  margin-bottom: 20px;
  color: #e74c3c;
}
</style>
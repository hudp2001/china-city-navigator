<template>
  <div class="province-container">
    <div class="breadcrumb">
      <router-link to="/" class="breadcrumb-link">首页</router-link>
      <span class="breadcrumb-separator">/</span>
      <span>{{ province?.name || '省份详情' }}</span>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>
    
    <div v-else-if="error" class="error-container">
      <p>{{ error }}</p>
      <button @click="loadData" class="retry-button">重试</button>
      <router-link to="/" class="back-button">返回首页</router-link>
    </div>
    
    <div v-else-if="province" class="province-detail">
      <div class="province-header">
        <h1>{{ province.name }}</h1>
        <p class="province-description">{{ province.description }}</p>
      </div>
      
      <div class="province-stats">
        <div class="stat-card">
          <div class="stat-value">{{ formatNumber(province.population) }}</div>
          <div class="stat-label">人口 (人)</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ formatNumber(province.area) }}</div>
          <div class="stat-label">面积 (平方公里)</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ formatNumber(province.gdp) }}</div>
          <div class="stat-label">GDP (亿元)</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ province.capital }}</div>
          <div class="stat-label">省会</div>
        </div>
      </div>
      
      <div class="map-container" ref="mapContainer"></div>
      
      <h2 class="cities-title">主要城市</h2>
      
      <div v-if="cities.length === 0" class="no-cities">
        <p>暂无城市数据</p>
      </div>
      
      <div v-else class="cities-grid">
        <div 
          v-for="city in cities" 
          :key="city.id" 
          class="city-card"
        >
          <div class="city-image-container">
            <div class="city-image-placeholder">{{ city.name.substring(0, 1) }}</div>
          </div>
          <div class="city-card-content">
            <h3>{{ city.name }}</h3>
            <p class="city-info">人口：{{ formatNumber(city.population) }}人</p>
            <p class="city-info">面积：{{ formatNumber(city.area) }}平方公里</p>
            <p class="city-attractions">
              <span class="attractions-label">景点：</span>
              {{ city.attractions.slice(0, 3).join('、') }}
              <span v-if="city.attractions.length > 3">等</span>
            </p>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else class="not-found">
      <h2>未找到省份信息</h2>
      <router-link to="/" class="back-button">返回首页</router-link>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { loadProvinceData, loadCitiesByProvince } from '../services/data-loader'
import { initMap, addCityMarker } from '../services/map-service'

export default {
  name: 'ProvincePage',
  setup() {
    const route = useRoute()
    const provinceId = ref(route.params.id)
    const province = ref(null)
    const cities = ref([])
    const loading = ref(true)
    const error = ref(null)

    const mapContainer = ref(null)

    const loadData = async () => {
      loading.value = true
      error.value = null
      
      try {
        // 加载省份数据
        const provinceData = await loadProvinceData(provinceId.value)
        province.value = provinceData
        
        if (!provinceData) {
          error.value = '未找到该省份的数据'
          return
        }
        
        // 加载城市数据
        const citiesData = await loadCitiesByProvince(provinceId.value)
        cities.value = citiesData
        
        // 初始化地图
        if (mapContainer.value) {
          const map = await initMap(mapContainer.value, [provinceData.longitude, provinceData.latitude], 7)
          
          // 添加城市标记
          citiesData.forEach(city => {
            addCityMarker(map, [city.longitude, city.latitude], city.name)
          })
        }
      } catch (err) {
        console.error('Failed to load province data:', err)
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
    watch(() => route.params.id, (newId) => {
      provinceId.value = newId
      loadData()
    })

    return {
      provinceId,
      province,
      cities,
      loading,
      error,
      loadData,
      formatNumber,
      mapContainer
    }
  }
}
</script>

<style scoped>
.province-container {
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

.province-header {
  margin-bottom: 30px;
}

.province-header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
  color: #333;
}

.province-description {
  font-size: 1.1rem;
  color: #555;
  line-height: 1.6;
}

.province-stats {
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

.cities-title {
  font-size: 1.8rem;
  margin-bottom: 20px;
  color: #333;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 10px;
}

.no-cities {
  text-align: center;
  padding: 30px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.cities-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.city-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  text-decoration: none;
  color: inherit;
  display: flex;
  flex-direction: column;
}

.city-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.city-image-container {
  height: 150px;
  background-color: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.city-image-placeholder {
  font-size: 3rem;
  color: white;
  background-color: #3498db;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.city-card-content {
  padding: 20px;
  flex-grow: 1;
}

.city-card h3 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #333;
  font-size: 1.3rem;
}

.city-info {
  color: #666;
  margin: 5px 0;
  font-size: 0.9rem;
}

.city-attractions {
  margin-top: 10px;
  color: #666;
  font-size: 0.9rem;
  line-height: 1.4;
}

.attractions-label {
  color: #555;
  font-weight: 500;
}

.not-found {
  text-align: center;
  padding: 50px 20px;
}

.not-found h2 {
  margin-bottom: 20px;
  color: #e74c3c;
}
.map-container {
  height: 400px;
  width: 100%;
  margin-bottom: 40px;
  border-radius: 8px;
  overflow: hidden;
}
</style>
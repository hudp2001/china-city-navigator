<template>
  <div class="main-layout">
    <div class="content-container">
      <aside class="sidebar">
        <TreeMenu @map-navigate="handleMapNavigate" @province-select="handleProvinceSelect" />
      </aside>
      <div class="city-card-list-container">
        <CityCardList :cities="cities" @city-select="handleCitySelect" />
      </div>
      <div class="map-container">
        <MapViewer ref="mapViewer" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import TreeMenu from './TreeMenu.vue'
import MapViewer from './MapViewer.vue'
import CityCardList from './CityCardList.vue'
import { loadCitiesByProvince } from '../services/data-loader'

const mapViewer = ref(null)
const cities = ref([]) // 添加 cities 变量的定义

// 处理地图导航事件
const handleMapNavigate = (navigationData) => {
  if (mapViewer.value && mapViewer.value.setMapCenter) {
    mapViewer.value.setMapCenter(navigationData.center, navigationData.zoom)
  }
}

// 处理城市卡片选择事件
const handleCitySelect = (city) => {
  console.log('City selected:', city); // 调试信息
  // 如果城市数据中有位置信息，则定位到该城市
  if (city.location) {
    handleMapNavigate({
      center: city.location,
      zoom: 12
    })
  }
}

// 处理省份选择事件
const handleProvinceSelect = async (province) => {
  try {
    // 加载省份的城市数据
    const cityData = await loadCitiesByProvince(province.id)
    // 更新城市卡片列表
    cities.value = cityData
  } catch (error) {
    console.error(`加载${province.name}的城市数据失败:`, error)
    // 出错时清空城市列表
    cities.value = []
  }
}

// 组件挂载后默认加载北京的数据
onMounted(async () => {
  try {
    // 加载北京的城市数据
    const beijingData = await loadCitiesByProvince('beijing')
    if (beijingData && beijingData.length > 0) {
      cities.value = beijingData
    }
  } catch (error) {
    console.error('加载北京城市数据失败:', error)
  }
})
</script>

<style scoped>
.main-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.content-container {
  display: flex;
  flex: 1;
  height: calc(100vh - 80px);
  padding: 0 5px;
  box-sizing: border-box;
}

.sidebar {
  flex: 0 0 160px;
  min-width: 160px;
  background-color: var(--color-background-soft, #f8f9fa);
  border-right: 1px solid var(--color-border, #e9ecef);
  overflow-y: auto;
  height: 100%;
  max-height: calc(100vh - 80px);
  box-sizing: border-box;
  padding-top: 0.5rem;
}

.city-card-list-container {
  flex: 1;
  height: 100%;
  overflow-y: auto;
  padding: 2px;
  background-color: #f5f5f5;
  min-height: 0;
  position: relative; /* 添加定位上下文 */
  z-index: 1; /* 设置较低的z-index */
}

.map-container {
  flex: 0 0 765px; /* 从600px减小到500px，进一步减少空白空间 */
  height: 100%;
  background-color: var(--color-background-mute, #f5f5f5);
  padding-left: 5px; /* 添加左边距，使地图不紧贴城市卡片 */
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .sidebar {
    min-width: 150px;
  }
}

@media (max-width: 768px) {
  .content-container {
    flex-direction: column;
  }
  
  .sidebar,
  .city-card-list-container {
    width: 100%;
    min-width: auto;
    height: 300px;
  }
  
  .map-container {
    flex: 1;
    height: auto;
  }
}
</style>
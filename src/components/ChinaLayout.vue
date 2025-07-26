<template>
  <div class="china-layout">
    <header class="header">
      <div class="header-content">
        <div class="header-left"></div>
        <router-link to="/" class="logo">中国省市百科导航</router-link>
        <div class="user-menu">
          <button @click.stop="toggleUserMenu" class="user-menu-button">
            系统
          </button>
          <div v-show="showUserMenu" class="user-menu-dropdown" ref="userMenuDropdown" @click.stop>
            <button @click="toggleHeatmap" class="menu-item">
              {{ heatmapActive ? '关闭去过热力图' : '开启去过热力图' }}
            </button>
            <button @click="toggleRanHeatmap" class="menu-item">
              {{ ranHeatmapActive ? '关闭跑过热力图' : '开启跑过热力图' }}
            </button>
            <button @click="toggleCollectedHeatmap" class="menu-item">
              {{ collectedHeatmapActive ? '关闭收藏热力图' : '开启收藏热力图' }}
            </button>
            <button @click="toggleMapExpansion" class="menu-item">
              {{ mapExpanded ? '恢复地图' : '放大地图' }}
            </button>
            <button @click="exportStatus" class="menu-item">
              导出状态
            </button>
            <button @click="clearAllStatus" class="menu-item">
              清除所有状态
            </button>
          </div>
        </div>
      </div>
    </header>
    
    <main class="main-content">
      <div class="content-container">
        <aside class="sidebar">
          <TreeMenu @map-navigate="handleMapNavigate" @province-select="handleProvinceSelect" />
        </aside>
        <div class="city-card-list-container" :class="{ hidden: mapExpanded }">
          <CityCardList :cities="cities" @city-select="handleCitySelect" @city-status-change="handleCityStatusChange" />
        </div>
        <div class="map-container" :class="{ expanded: mapExpanded }">
          <MapViewer ref="mapViewer" />
        </div>
      </div>
    </main>
    
    <footer class="footer">
      <div class="footer-content">
        <p>&copy; {{ currentYear }} 中国省市百科导航</p>
      </div>
    </footer>
    
    <!-- 热力图模态框 -->
    <div v-if="showHeatmapModal" class="heatmap-modal" @click="closeHeatmapModal">
      <div class="heatmap-modal-content" @click.stop>
        <div class="heatmap-modal-header">
          <h2>去过/跑过城市热力图</h2>
          <button @click="closeHeatmapModal" class="close-button">&times;</button>
        </div>
        <div class="heatmap-modal-body">
          <div v-if="loadingCities" class="loading">
            <p>加载中...</p>
          </div>
          <div v-else>
            <p v-if="visitedCities.length === 0">您还没有标记任何去过或跑过的城市。</p>
            <div v-else class="heatmap-content">
              <div class="heatmap-stats">
                <p>总共去过/跑过 <strong>{{ visitedCities.length }}</strong> 个城市</p>
              </div>
              <div class="heatmap-list">
                <h3>城市列表：</h3>
                <ul>
                  <li v-for="city in visitedCities" :key="city.id">
                    {{ city.name }}
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 确认清除状态模态框 -->
    <div v-if="showClearConfirm" class="confirm-modal" @click="closeClearConfirm">
      <div class="heatmap-modal-content" @click.stop>
        <div class="confirm-modal-header">
          <h2>确认清除</h2>
          <button @click="closeClearConfirm" class="close-button">&times;</button>
        </div>
        <div class="confirm-modal-body">
          <p>确定要清除所有"去过"、"收藏"、"跑过"状态吗？此操作不可撤销。</p>
          <div class="confirm-modal-actions">
            <button @click="closeClearConfirm" class="btn-cancel">取消</button>
            <button @click="confirmClearAllStatus" class="btn-confirm">确定</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import TreeMenu from './TreeMenu.vue'
import CityCardList from './CityCardList.vue'
import MapViewer from './MapViewer.vue'
import { getVisitedAndRanCities, getRanCities, getCollectedCities, clearAllCityStatus } from '../services/user-status'
import { loadAllCities, loadCitiesByProvince, loadAllProvinces } from '../services/data-loader'
import * as XLSX from 'xlsx'

const currentYear = computed(() => new Date().getFullYear())

// 用户菜单状态
const showUserMenu = ref(false)
const userMenuDropdown = ref(null)

// 热力图模态框状态
const showHeatmapModal = ref(false)
const visitedCities = ref([])
const loadingCities = ref(false)

// 热力图激活状态（现在可以同时激活多个）
const heatmapActive = ref(false)
const ranHeatmapActive = ref(false)
const collectedHeatmapActive = ref(false)

// 存储各类城市数据
const visitedCityData = ref([])
const ranCityData = ref([])
const collectedCityData = ref([])

// 确认清除状态模态框
const showClearConfirm = ref(false)

// 地图和城市相关
const mapViewer = ref(null)
const cities = ref([]) // 添加 cities 变量的定义

// 地图放大状态
const mapExpanded = ref(false)

// 所有城市数据
let allCitiesData = {}

// 切换用户菜单显示状态
const toggleUserMenu = (event) => {
  if (event) {
    event.stopPropagation();
  }
  showUserMenu.value = !showUserMenu.value
}

// 隐藏用户菜单
const hideUserMenu = () => {
  showUserMenu.value = false
}

// 切换去过热力图标识
const toggleHeatmap = () => {
  showUserMenu.value = false
  // 切换热力图状态
  heatmapActive.value = !heatmapActive.value
  
  // 更新地图显示
  updateMapWithAllHeatmaps()
}

// 切换跑过热力图标识
const toggleRanHeatmap = () => {
  showUserMenu.value = false
  // 切换跑过热力图状态
  ranHeatmapActive.value = !ranHeatmapActive.value
  
  // 更新地图显示
  updateMapWithAllHeatmaps()
}

// 切换收藏热力图标识
const toggleCollectedHeatmap = () => {
  showUserMenu.value = false
  // 切换收藏热力图状态
  collectedHeatmapActive.value = !collectedHeatmapActive.value
  
  // 更新地图显示
  updateMapWithAllHeatmaps()
}

// 更新地图显示所有激活的热力图
const updateMapWithAllHeatmaps = async () => {
  try {
    // 如果没有任何热力图激活，则恢复默认地图
    if (!heatmapActive.value && !ranHeatmapActive.value && !collectedHeatmapActive.value) {
      if (mapViewer.value && typeof mapViewer.value.restoreDefaultMap === 'function') {
        mapViewer.value.restoreDefaultMap()
      }
      return;
    }
    
    // 如果还没有加载所有城市数据，则加载
    if (Object.keys(allCitiesData).length === 0) {
      await loadAllCityData()
    }
    
    // 根据激活状态加载相应的城市数据
    if (heatmapActive.value && visitedCityData.value.length === 0) {
      const visitedCityIds = getVisitedAndRanCities()
      visitedCityData.value = visitedCityIds.map(id => allCitiesData[id]).filter(city => city)
    }
    
    if (ranHeatmapActive.value && ranCityData.value.length === 0) {
      const ranCityIds = getRanCities()
      ranCityData.value = ranCityIds.map(id => allCitiesData[id]).filter(city => city)
    }
    
    if (collectedHeatmapActive.value && collectedCityData.value.length === 0) {
      const collectedCityIds = getCollectedCities()
      collectedCityData.value = collectedCityIds.map(id => allCitiesData[id]).filter(city => city)
    }
    
    // 在地图上显示所有激活的热力图
    if (mapViewer.value && typeof mapViewer.value.showAllCitiesWithMultipleHeatmaps === 'function') {
      const allCityData = Object.values(allCitiesData)
      mapViewer.value.showAllCitiesWithMultipleHeatmaps(
        allCityData, 
        heatmapActive.value ? visitedCityData.value : [], 
        ranHeatmapActive.value ? ranCityData.value : [], 
        collectedHeatmapActive.value ? collectedCityData.value : []
      )
    }
  } catch (error) {
    console.error('更新热力图显示失败:', error)
  }
}

// 当在城市卡片上更改状态时更新地图
const updateMapWithCityStatus = async (cityId) => {
  // 只有当任一热力图激活时才更新地图
  if (!heatmapActive.value && !ranHeatmapActive.value && !collectedHeatmapActive.value) {
    return;
  }
  
  try {
    // 如果还没有加载所有城市数据，则加载
    if (Object.keys(allCitiesData).length === 0) {
      await loadAllCityData()
    }
    
    // 更新对应的状态数据
    if (heatmapActive.value) {
      // 更新去过/跑过状态数据
      const visitedCityIds = getVisitedAndRanCities()
      visitedCityData.value = visitedCityIds.map(id => allCitiesData[id]).filter(city => city)
    }
    
    if (ranHeatmapActive.value) {
      // 更新跑过状态数据
      const ranCityIds = getRanCities()
      ranCityData.value = ranCityIds.map(id => allCitiesData[id]).filter(city => city)
    }
    
    if (collectedHeatmapActive.value) {
      // 更新收藏状态数据
      const collectedCityIds = getCollectedCities()
      collectedCityData.value = collectedCityIds.map(id => allCitiesData[id]).filter(city => city)
    }
    
    // 在地图上显示所有激活的热力图
    if (mapViewer.value && typeof mapViewer.value.showAllCitiesWithMultipleHeatmaps === 'function') {
      const allCityData = Object.values(allCitiesData)
      mapViewer.value.showAllCitiesWithMultipleHeatmaps(
        allCityData, 
        heatmapActive.value ? visitedCityData.value : [], 
        ranHeatmapActive.value ? ranCityData.value : [], 
        collectedHeatmapActive.value ? collectedCityData.value : []
      )
    }
  } catch (error) {
    console.error('更新城市状态显示失败:', error)
  }
}

// 显示热力图清单（点击菜单项第二次时弹出清单）
const showHeatmap = async () => {
  showUserMenu.value = false
  
  // 只有在热力图已激活时才显示清单
  if (heatmapActive.value) {
    try {
      showHeatmapModal.value = true
      loadingCities.value = true
      
      // 如果还没有加载所有城市数据，则加载
      if (Object.keys(allCitiesData).length === 0) {
        await loadAllCityData()
      }
      
      // 获取用户标记为去过或跑过的城市详情
      visitedCities.value = getVisitedAndRanCitiesDetails(allCitiesData)
    } catch (error) {
      console.error('获取热力图数据失败:', error)
    } finally {
      loadingCities.value = false
    }
  } else {
    // 如果热力图未激活，则激活它
    await toggleHeatmap()
  }
}

// 显示清除确认对话框
const clearAllStatus = () => {
  showUserMenu.value = false
  showClearConfirm.value = true
}

// 关闭清除确认对话框
const closeClearConfirm = () => {
  showClearConfirm.value = false
}

// 确认清除所有状态
const confirmClearAllStatus = () => {
  clearAllCityStatus()
  showClearConfirm.value = false
  // 显示一个简单的提示
  alert('所有状态已清除')
  
  // 重置所有数据
  visitedCityData.value = []
  ranCityData.value = []
  collectedCityData.value = []
  
  // 更新地图显示
  updateMapWithAllHeatmaps()
}

// 加载所有城市数据
const loadAllCityData = async () => {
  try {
    // 使用loadAllCities函数加载所有城市数据
    allCitiesData = await loadAllCities("all")
    console.log('加载所有城市数据完成，共', Object.keys(allCitiesData).length, '个城市')
  } catch (error) {
    console.error('加载所有城市数据失败:', error)
  }
}

// 关闭热力图模态框
const closeHeatmapModal = () => {
  showHeatmapModal.value = false
  heatmapActive.value = false
  
  // 更新地图显示
  updateMapWithAllHeatmaps()
}

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

// 处理城市状态更改事件
const handleCityStatusChange = (statusData) => {
  // 只有当任一热力图激活时才更新地图
  if (heatmapActive.value || ranHeatmapActive.value || collectedHeatmapActive.value) {
    // 延迟更新地图，确保状态已保存到localStorage
    setTimeout(() => {
      updateMapWithCityStatus(statusData.cityId);
    }, 100);
  }
}

// 导出状态为Excel文件
const exportStatus = async () => {
  showUserMenu.value = false;
  
  try {
    // 如果还没有加载所有城市数据，则加载
    if (Object.keys(allCitiesData).length === 0) {
      await loadAllCityData();
    }
    
    // 获取所有省份数据
    const provinces = await loadAllProvinces();
    const provinceMap = {};
    provinces.forEach(province => {
      provinceMap[province.id] = province.name;
    });
    
    // 获取所有状态数据
    const visitedCityIds = getVisitedAndRanCities();
    const ranCityIds = getRanCities();
    const collectedCityIds = getCollectedCities();
    
    // 获取详细城市信息
    const visitedCities = visitedCityIds.map(id => allCitiesData[id]).filter(city => city);
    const ranCities = ranCityIds.map(id => allCitiesData[id]).filter(city => city);
    const collectedCities = collectedCityIds.map(id => allCitiesData[id]).filter(city => city);
    
    // 按省份组织数据
    const organizeByProvince = (cities) => {
      const provinceMap = {};
      
      cities.forEach(city => {
        // 从城市ID中提取省份ID (格式: 省份ID_城市ID)
        const provinceId = city.id.split('_')[0];
        const cityName = city.name;
        
        if (!provinceMap[provinceId]) {
          provinceMap[provinceId] = [];
        }
        
        provinceMap[provinceId].push(cityName);
      });
      
      return provinceMap;
    };
    
    // 组织数据
    const visitedByProvince = organizeByProvince(visitedCities);
    const ranByProvince = organizeByProvince(ranCities);
    const collectedByProvince = organizeByProvince(collectedCities);
    
    // 创建工作簿
    const wb = XLSX.utils.book_new();
    
    // 创建去过城市工作表
    const visitedData = [];
    for (const [provinceId, cities] of Object.entries(visitedByProvince)) {
      const provinceName = provinceMap[provinceId] || provinceId;
      cities.forEach(city => {
        visitedData.push([provinceName, city]);
      });
    }
    const visitedWs = XLSX.utils.aoa_to_sheet([['省份', '去过城市'], ...visitedData]);
    XLSX.utils.book_append_sheet(wb, visitedWs, '去过城市');
    
    // 创建跑过城市工作表
    const ranData = [];
    for (const [provinceId, cities] of Object.entries(ranByProvince)) {
      const provinceName = provinceMap[provinceId] || provinceId;
      cities.forEach(city => {
        ranData.push([provinceName, city]);
      });
    }
    const ranWs = XLSX.utils.aoa_to_sheet([['省份', '跑过城市'], ...ranData]);
    XLSX.utils.book_append_sheet(wb, ranWs, '跑过城市');
    
    // 创建收藏城市工作表
    const collectedData = [];
    for (const [provinceId, cities] of Object.entries(collectedByProvince)) {
      const provinceName = provinceMap[provinceId] || provinceId;
      cities.forEach(city => {
        collectedData.push([provinceName, city]);
      });
    }
    const collectedWs = XLSX.utils.aoa_to_sheet([['省份', '收藏城市'], ...collectedData]);
    XLSX.utils.book_append_sheet(wb, collectedWs, '收藏城市');
    
    // 导出文件
    XLSX.writeFile(wb, '城市状态导出.xlsx');
  } catch (error) {
    console.error('导出状态失败:', error);
    alert('导出失败，请查看控制台了解详细信息');
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

// 点击外部关闭菜单
const handleClickOutside = (event) => {
  if (userMenuDropdown.value && !userMenuDropdown.value.contains(event.target)) {
    hideUserMenu()
  }
}

// 切换地图放大/恢复状态
const toggleMapExpansion = () => {
  showUserMenu.value = false
  mapExpanded.value = !mapExpanded.value
  
  // 触发地图大小调整
  setTimeout(() => {
    if (mapViewer.value && mapViewer.value.map) {
      mapViewer.value.map.resize()
    }
  }, 300)
}

// 组件挂载后默认加载北京的数据
onMounted(async () => {
  document.addEventListener('click', handleClickOutside)
  
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

// 卸载前移除事件监听器
onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
  
  // 确保在组件卸载时清理热力图状态
  if ((heatmapActive.value || ranHeatmapActive.value || collectedHeatmapActive.value) && 
      mapViewer.value && typeof mapViewer.value.restoreDefaultMap === 'function') {
    mapViewer.value.restoreDefaultMap();
  }
})
</script>

<style scoped>
.china-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.header {
  background-color: #3498db;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100; /* 确保头部在最上层 */
  height: 70px; /* 明确设置头部高度 */
  display: flex;
  align-items: center;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 15px 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  width: 100%;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  text-decoration: none;
  margin: 0 20px; /* 添加左右间距 */
}

.header-left {
  flex: 1; /* 占据左侧空间 */
}

.user-menu {
  flex: 1; /* 占据右侧空间 */
  display: flex;
  justify-content: flex-end; /* 菜单按钮靠右对齐 */
}

.user-menu-button {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.user-menu-button:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

.user-menu-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  min-width: 150px;
  overflow: visible;
}

.menu-item {
  display: block;
  width: 100%;
  padding: 18px 20px;
  border: none;
  background: none;
  text-align: left;
  cursor: pointer;
  font-size: 0.95rem;
  color: #333;
  transition: background-color 0.2s;
  line-height: 1.3;
  min-height: 56px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  box-sizing: border-box; /* 确保padding包含在高度内 */
  display: flex; /* 使用flex布局 */
  align-items: center; /* 垂直居中 */
}

.menu-item:hover {
  background-color: #f5f5f5;
}

.menu-item.active {
  background-color: #e3f2fd;
  color: #1976d2;
  font-weight: 500;
}

.menu-check {
  color: #28a745;
  font-weight: bold;
  margin-right: 8px;
}

.main-content {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.content-container {
  display: flex;
  flex: 1;
  overflow: hidden;
  max-width: 100%;
}

.sidebar {
  width: 150px;
  background-color: #f8f9fa;
  border-right: 1px solid #e0e0e0;
  overflow-y: auto;
  flex-shrink: 0;
}

.city-card-list-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  min-width: 0;
}

.city-card-list-container.hidden {
  display: none;
}

.map-container {
  width: 40%;
  min-width: 400px;
  background-color: #f0f0f0;
  position: relative;
  transition: width 0.3s ease; /* 添加过渡动画 */
}

/* 地图放大时的样式 */
.map-container.expanded {
  width: calc(100% - 150px); /* 减去侧边栏宽度，占据整个右侧区域 */
  position: absolute;
  right: 0;
  top: 0;
  height: calc(100% - 70px); /* 减去头部高度，避免遮挡头部 */
  z-index: 90; /* 降低z-index值，确保不遮挡头部菜单 */
  margin-top: 70px; /* 添加顶部边距，避免遮挡头部 */
  left: auto; /* 添加此属性以确保右侧对齐 */
  bottom: auto; /* 添加此属性以确保顶部对齐 */
}

.footer {
  background-color: #f8f9fa;
  border-top: 1px solid #e0e0e0;
  padding: 20px 0;
  text-align: center;
}

.footer-content p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

/* 热力图模态框样式 */
.heatmap-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.heatmap-modal-content {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.heatmap-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e0e0e0;
}

.heatmap-modal-header h2 {
  margin: 0;
  color: #333;
  font-size: 1.5rem;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #999;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.2s, color 0.2s;
}

.close-button:hover {
  background-color: #f0f0f0;
  color: #666;
}

.heatmap-modal-body {
  padding: 20px;
  overflow-y: auto;
  flex: 1;
}

.heatmap-content {
  margin-top: 10px;
}

.heatmap-stats {
  margin-bottom: 20px;
  padding: 10px;
  background-color: #f0f8ff;
  border-radius: 4px;
  border-left: 4px solid #4A90E2;
}

.heatmap-list h3 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #333;
}

.heatmap-list ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.heatmap-list li {
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
  color: #555;
}

.heatmap-list li:last-child {
  border-bottom: none;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #666;
}

/* 确认清除状态模态框样式 */
.confirm-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.confirm-modal-content {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  max-width: 500px;
  width: 90%;
  overflow: hidden;
}

.confirm-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e0e0e0;
}

.confirm-modal-header h2 {
  margin: 0;
  color: #333;
  font-size: 1.5rem;
}

.confirm-modal-body {
  padding: 20px;
}

.confirm-modal-body p {
  margin: 0 0 20px 0;
  color: #555;
  line-height: 1.5;
}

.confirm-modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.btn-cancel,
.btn-confirm {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.btn-cancel {
  background-color: #f0f0f0;
  color: #333;
}

.btn-cancel:hover {
  background-color: #e0e0e0;
}

.btn-confirm {
  background-color: #dc3545;
  color: white;
}

.btn-confirm:hover {
  background-color: #c82333;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .content-container {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid #e0e0e0;
  }
  
  .city-card-list-container {
    padding: 10px;
  }
  
  .map-container {
    width: 100%;
    min-width: auto;
    height: 400px;
  }
}

@media (max-width: 768px) {
  .content-container {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid #e0e0e0;
  }
  
  .city-card-list-container {
    padding: 10px;
  }
  
  .map-container {
    width: 100%;
    min-width: auto;
    height: 400px;
  }
}
</style>

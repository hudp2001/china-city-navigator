<template>
  <div class="map-viewer">
    <div id="map" ref="mapContainer"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { initMap, addCityMarker } from '../services/map-service'

const mapContainer = ref(null)
const mapInstance = ref(null)
let markers = [] // 存储所有标记
let defaultMarkers = [] // 存储默认标记
let circles = [] // 存储圆形背景标记

onMounted(async () => {
  try {
    console.log('开始初始化地图...')
    // 确保DOM已更新
    await new Promise(resolve => setTimeout(resolve, 100));
    
    // 初始化地图 (使用北京中心点)
    const map = await initMap('map', [116.397428, 39.90923], 5)
    console.log('地图初始化成功:', map)
    // 保存地图实例以便后续操作
    mapInstance.value = map
    mapContainer.value = document.getElementById('map')
    
    // 不再添加默认城市标记
  } catch (error) {
    console.error('地图初始化失败:', error)
  }
})

// 设置地图中心点和缩放级别
const setMapCenter = (center, zoom) => {
  if (mapInstance.value) {
    mapInstance.value.setCenter(center)
    mapInstance.value.setZoom(zoom)
  }
}

// 显示所有城市并根据不同的状态显示不同的背景色
const showAllCitiesWithMultipleHeatmaps = (allCities, visitedCities, ranCities, collectedCities) => {
  if (!mapInstance.value || !allCities || !Array.isArray(allCities)) {
    console.warn('无法显示城市热力图：地图未初始化或城市数据无效')
    return
  }

  // 清除现有的热力图标记
  clearHeatmapMarkers()
  
  // 创建一个映射来快速查找城市状态
  const visitedMap = new Map(visitedCities.map(city => [city.id, city]));
  const ranMap = new Map(ranCities.map(city => [city.id, city]));
  const collectedMap = new Map(collectedCities.map(city => [city.id, city]));
  
  // 添加所有城市的标记
  allCities.forEach(city => {
    if (city.location && city.name) {
      try {
        // 检查城市的各种状态
        const isVisited = visitedMap.has(city.id);
        const isRan = ranMap.has(city.id);
        const isCollected = collectedMap.has(city.id);
        
        // 创建标记
        const marker = new window.AMap.Marker({
          position: city.location,
          title: city.name,
          animation: 'AMAP_ANIMATION_DROP',
          clickable: true,
          // 根据状态使用不同颜色的标记
          icon: new window.AMap.Icon({
            size: new window.AMap.Size(20, 20),
            image: '//a.amap.com/jsapi_demos/static/demo-center/icons/poi-marker-default.png',
            imageSize: new window.AMap.Size(20, 20),
            imageOffset: isVisited || isRan 
              ? new window.AMap.Pixel(-54, -90) // 红色标记（去过或跑过）
              : isCollected 
                ? new window.AMap.Pixel(-108, -90) // 绿色标记（收藏）
                : new window.AMap.Pixel(-28, -90)  // 蓝色标记（未访问）
          })
        })
        
        // 添加背景圆圈（可以同时显示多种类型）
        const circlesToAdd = [];
        
        // 添加去过背景（深蓝色，50公里）
        if (isVisited) {
          const visitedCircle = new window.AMap.Circle({
            center: city.location,
            radius: 50000, // 50公里（从100公里修改为50公里）
            fillColor: '#0000FF', // 深蓝色
            fillOpacity: 0.3,
            strokeColor: '#0000FF',
            strokeOpacity: 0.5,
            strokeWeight: 1
          });
          circlesToAdd.push(visitedCircle);
        }
        
        // 添加跑过背景（红色，40公里）
        if (isRan) {
          const ranCircle = new window.AMap.Circle({
            center: city.location,
            radius: 40000, // 40公里（从70公里修改为40公里）
            fillColor: '#FF0000', // 红色
            fillOpacity: 0.3,
            strokeColor: '#FF0000',
            strokeOpacity: 0.5,
            strokeWeight: 1
          });
          circlesToAdd.push(ranCircle);
        }
        
        // 添加收藏背景（绿色，30公里）
        if (isCollected) {
          const collectedCircle = new window.AMap.Circle({
            center: city.location,
            radius: 30000, // 30公里（从50公里修改为30公里）
            fillColor: '#00FF00', // 绿色
            fillOpacity: 0.3,
            strokeColor: '#00FF00',
            strokeOpacity: 0.5,
            strokeWeight: 1
          });
          circlesToAdd.push(collectedCircle);
        }
        
        // 添加所有背景圆圈到地图
        circlesToAdd.forEach(circle => {
          if (mapInstance.value) {
            mapInstance.value.add(circle);
            circles.push(circle);
          }
        });
        
        // 添加到地图
        if (mapInstance.value) {
          mapInstance.value.add(marker)
          markers.push({ 
            marker, 
            city: city.name, 
            location: city.location,
            circles: circlesToAdd // 保存所有圆形背景引用
          })
        }
        
        // 创建信息窗口
        const statusText = [];
        if (isVisited) statusText.push('已去过');
        if (isRan) statusText.push('已跑过');
        if (isCollected) statusText.push('已收藏');
        const displayStatus = statusText.length > 0 ? statusText.join(', ') : '未访问';
        
        const infoWindow = new window.AMap.InfoWindow({
          content: `<div class="marker-info"><strong>${city.name}</strong><br/>${displayStatus}</div>`,
          offset: new window.AMap.Pixel(0, -30)
        })
        
        // 点击标记时打开信息窗口
        marker.on('click', () => {
          infoWindow.open(mapInstance.value, marker.getPosition())
        })
      } catch (error) {
        console.error(`添加标记失败 (${city.name}):`, error)
      }
    }
  })
  
  console.log(`已显示 ${allCities.length} 个城市，其中去过${visitedCities.length}个，跑过${ranCities.length}个，收藏${collectedCities.length}个`)
}

// 清除热力图标记
const clearHeatmapMarkers = () => {
  markers.forEach(item => {
    if (mapInstance.value) {
      mapInstance.value.remove(item.marker)
      // 同时移除所有圆形背景
      if (item.circles && Array.isArray(item.circles)) {
        item.circles.forEach(circle => {
          mapInstance.value.remove(circle);
        });
      }
    }
  })
  
  markers = []
  circles = [] // 清空圆形背景数组
  console.log('已清除所有热力图标记和背景')
}

// 恢复地图默认状态
const restoreDefaultMap = () => {
  // 清除热力图标记
  clearHeatmapMarkers()
  
  // 不再添加默认标记
  console.log('地图已恢复默认状态')
}

// 暴露方法给父组件调用
defineExpose({
  setMapCenter,
  showAllCitiesWithMultipleHeatmaps,
  restoreDefaultMap
})

</script>

<style scoped>
.map-viewer {
  width: 100%;
  position: relative;
  height: 100%;
}
#map {
  width: 100%;
  height: 100%;
}
/* 添加标记信息窗口样式 */
.marker-info {
  padding: 5px 10px;
  font-weight: bold;
}
</style>
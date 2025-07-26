<template>
  <div class="map-viewer">
    <div class="map-header">
      <h3>地图导航</h3>
      <div class="map-controls">
        <button
          @click="showHeatmap = !showHeatmap"
          :class="{ active: showHeatmap }"
          class="heatmap-toggle"
        >
          热力图
        </button>
        <button @click="exportMap" class="export-btn">
          导出地图
        </button>
      </div>
    </div>
    <div id="map-container" class="map-container"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import html2canvas from 'html2canvas'
import AMapLoader from '@amap/amap-jsapi-loader'
const showHeatmap = ref(false)
let map = null
let heatmapLayer = null
let AMap = null

const emit = defineEmits(['map-ready'])

onMounted(() => {
  initMap()
})

onUnmounted(() => {
  if (map) {
    map.destroy()
  }
})

const initMap = async () => {
  try {
    // 使用AMapLoader加载高德地图API
    AMap = await AMapLoader.load({
      key: "e40de3c00a562a2b238ca8986aacf68f", // 请替换为实际的高德地图API Key
      version: "1.4.15", // 指定要加载的API版本
      plugins: ['AMap.Scale', 'AMap.ToolBar', 'AMap.ControlBar', 'AMap.Geocoder', 'AMap.Heatmap']
    })
  } catch (error) {
    console.error('高德地图API加载失败:', error)
    return
  }

  // 创建地图实例
  map = new AMap.Map('map-container', {
    zoom: 5,
    center: [108.953098, 34.2778], // 中国地理中心
    mapStyle: 'amap://styles/normal',
    features: ['bg', 'road', 'building', 'point'],
    viewMode: '2D'
  })

  // 添加地图控件
  map.addControl(new AMap.Scale())
  map.addControl(new AMap.ToolBar())
  map.addControl(new AMap.ControlBar())

  // 地图加载完成后的回调
  map.on('complete', () => {
    console.log('地图加载完成')
    emit('map-ready', map)
  })

  // 地图点击事件
  map.on('click', (e) => {
    console.log('地图点击位置:', e.lnglat)
  })
}

// 定位到指定城市
const locateToCity = (cityName, zoomLevel = 12) => {
  if (!map || !AMap) {
    console.error('高德地图API未加载')
    return
  }

  // 使用高德地图的地理编码服务
  AMap.plugin('AMap.Geocoder', () => {
    const geocoder = new AMap.Geocoder()
    
    geocoder.getLocation(cityName, (status, result) => {
      if (status === 'complete' && result.geocodes.length > 0) {
        const location = result.geocodes[0].location
        map.setCenter(location)
        map.setZoom(zoomLevel)
        
        // 添加标记
        const marker = new AMap.Marker({
          position: location,
          title: cityName,
          animation: 'AMAP_ANIMATION_DROP'
        })
        map.add(marker)
        
        // 添加信息窗体
        const infoWindow = new AMap.InfoWindow({
          content: `<div style="padding: 10px;"><strong>${cityName}</strong></div>`,
          offset: new AMap.Pixel(0, -30)
        })
        
        marker.on('click', () => {
          infoWindow.open(map, location)
        })
      }
    })
  })
}

// 定位到省份
const locateToProvince = (provinceName, zoomLevel = 8) => {
  locateToCity(provinceName, zoomLevel)
}

// 显示/隐藏热力图
const toggleHeatmap = () => {
  if (!map) return

  if (showHeatmap.value) {
    showHeatmapLayer()
  } else {
    hideHeatmapLayer()
  }
}

// 显示热力图层
const showHeatmapLayer = () => {
  if (heatmapLayer) {
    map.add(heatmapLayer)
    return
  }

  // 加载热力图插件
  AMap.plugin('AMap.Heatmap', () => {
    const heatmapData = generateHeatmapData()
    
    heatmapLayer = new AMap.Heatmap(map, {
      radius: 25,
      opacity: [0, 0.8],
      gradient: {
        0.4: 'blue',
        0.65: 'lime',
        0.85: 'yellow',
        1.0: 'red'
      }
    })
    
    heatmapLayer.setDataSet({
      data: heatmapData,
      max: 3
    })
  })
}

// 隐藏热力图层
const hideHeatmapLayer = () => {
  if (heatmapLayer) {
    map.remove(heatmapLayer)
  }
}

// 生成热力图数据（示例数据）
const generateHeatmapData = () => {
  // 示例热力图数据
  const data = [
    { lng: 116.405285, lat: 39.904989, count: 10 }, // 北京
    { lng: 121.472644, lat: 31.231706, count: 8 },  // 上海
    { lng: 113.280637, lat: 23.125178, count: 7 },  // 广州
    { lng: 114.085947, lat: 22.547, count: 6 },     // 深圳
    { lng: 118.767413, lat: 32.041544, count: 5 },  // 南京
    { lng: 120.153576, lat: 30.287459, count: 4 },  // 杭州
    { lng: 104.065735, lat: 30.659462, count: 3 }   // 成都
  ]
  
  return data
}

// 导出地图
const exportMap = async () => {
  if (!map) return
  
  try {
    const mapContainer = document.getElementById('map-container')
    const canvas = await html2canvas(mapContainer, {
      useCORS: true,
      scale: 2
    })
    
    // 创建下载链接
    const link = document.createElement('a')
    link.download = `china-map-${new Date().toISOString().split('T')[0]}.png`
    link.href = canvas.toDataURL()
    link.click()
  } catch (error) {
    console.error('导出地图失败:', error)
  }
}

// 监听热力图切换
watch(showHeatmap, (newVal) => {
  toggleHeatmap()
})

// 暴露方法给父组件
defineExpose({
  locateToCity,
  locateToProvince,
  toggleHeatmap,
  exportMap
})
</script>

<style scoped>
.map-viewer {
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: var(--bg-color, #ffffff);
}

.map-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid var(--border-color, #e0e0e0);
  background-color: var(--header-bg, #f8f9fa);
}

.map-controls {
  display: flex;
  gap: 8px;
}

.heatmap-toggle, .export-btn {
  padding: 6px 12px;
  border: 1px solid var(--border-color, #ccc);
  background-color: var(--button-bg, #fff);
  color: var(--button-color, #333);
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.heatmap-toggle:hover, .export-btn:hover {
  background-color: var(--button-hover-bg, #f0f0f0);
}

.heatmap-toggle.active {
  background-color: var(--primary-color, #007bff);
  color: white;
  border-color: var(--primary-color, #007bff);
}

.map-container {
  flex: 1;
  min-height: 0;
}
</style>
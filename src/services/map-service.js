/**
 * 地图服务模块 - 基于高德地图API
 * 提供地图初始化、标记添加和导出功能
 */
import AMapLoader from '@amap/amap-jsapi-loader'
import html2canvas from 'html2canvas'

// 高德地图初始化配置
const mapConfig = {
  key: 'e40de3c00a562a2b238ca8986aacf68f', // 请替换为实际的高德地图API Key
  version: '2.0',
  plugins: ['AMap.Scale', 'AMap.ToolBar', 'AMap.ControlBar']
}

let AMapInstance = null;

/**
 * 初始化地图
 * @param {string} containerId - 地图容器ID
 * @param {Array} initialCenter - 初始中心点坐标 [经度, 纬度]
 * @param {number} initialZoom - 初始缩放级别
 * @returns {Promise<Object>} - 返回地图实例
 */
export const initMap = async (containerId, initialCenter = [116.397428, 39.90923], initialZoom = 5) => {
  try {
    // 加载高德地图API
    const AMap = await AMapLoader.load(mapConfig)
    AMapInstance = AMap;
    
    // 创建地图实例
    const map = new AMap.Map(containerId, {
      viewMode: '2D',
      zoom: initialZoom,
      center: initialCenter,
      resizeEnable: true
    })
    
    // 添加地图控件
    map.addControl(new AMap.Scale())
    map.addControl(new AMap.ToolBar())
    map.addControl(new AMap.ControlBar({
      position: {
        right: '10px',
        top: '10px'
      }
    }))
    
    return map
  } catch (error) {
    console.error('高德地图加载失败:', error)
    throw error
  }
}

/**
 * 添加城市标记
 * @param {Object} map - 地图实例
 * @param {Array} cityLocation - 城市坐标 [经度, 纬度]
 * @param {string} cityName - 城市名称
 * @returns {Object} - 返回标记实例
 */
export const addCityMarker = (map, cityLocation, cityName) => {
  // 确保 AMap 对象已加载
  if (!AMapInstance) {
    throw new Error('高德地图 API 未正确加载')
  }
  
  // 创建标记
  const marker = new AMapInstance.Marker({
    position: cityLocation,
    title: cityName,
    animation: 'AMAP_ANIMATION_DROP',
    clickable: true
  })
  
  // 添加到地图
  map.add(marker)
  
  // 创建信息窗口
  const infoWindow = new AMapInstance.InfoWindow({
    content: `<div class="marker-info">${cityName}</div>`,
    offset: new AMapInstance.Pixel(0, -30)
  })
  
  // 点击标记时打开信息窗口
  marker.on('click', () => {
    infoWindow.open(map, marker.getPosition())
  })
  
  return marker
}

/**
 * 导出地图为图片
 * @param {HTMLElement} mapContainer - 地图容器元素
 * @returns {Promise<void>} - 导出完成的Promise
 */
export const exportMapToImage = async (mapContainer) => {
  try {
    // 使用html2canvas导出地图
    const canvas = await html2canvas(mapContainer, {
      useCORS: true,
      allowTaint: false,
      logging: false
    })
    
    // 转换为图片并下载
    const image = canvas.toDataURL('image/png')
    const link = document.createElement('a')
    link.href = image
    link.download = `map-export-${new Date().toISOString().slice(0, 10)}.png`
    link.click()
  } catch (error) {
    console.error('导出地图失败:', error)
    throw error
  }
}
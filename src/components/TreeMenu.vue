<template>
  <div class="tree-menu">
    <ul class="tree-root">
      <!-- 大区节点 -->
      <li v-for="(region, index) in regions" :key="index" class="tree-node region-node">
        <div 
          class="node-content" 
          @click="toggleRegion(region)"
          :class="{ 'highlighted': highlightedNode === region }"
        >
          <span class="node-toggle">
            {{ region.expanded ? '▼' : '▶' }}
          </span>
          <span class="node-label region-label">{{ region.name }}</span>
        </div>
        
        <!-- 省份/直辖市列表 -->
        <ul v-if="region.expanded" class="children">
          <li 
            v-for="(province, provinceIndex) in region.provinces" 
            :key="provinceIndex" 
            class="tree-node province-node"
            @click="selectProvince(province)"
            :class="{ 'highlighted': highlightedNode === province }"
          >
            <div class="node-content">
              <span class="node-label province-label">{{ province.name }}</span>
            </div>
          </li>
        </ul>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { regionData } from '../services/region-data'
import { loadCitiesByProvince } from '../services/data-loader'

// 使用统一的数据结构
const regions = ref(regionData)

const emit = defineEmits(['node-select', 'map-navigate', 'province-select'])
const highlightedNode = ref(null)

/**
 * 切换大区展开/折叠状态
 * 点击大区节点可展开/折叠对应省份列表，地图不发生变化
 */
const toggleRegion = (region) => {
  region.expanded = !region.expanded
  // 点击大区节点时，地图不发生变化
  highlightedNode.value = region
}

/**
 * 选择省份或直辖市
 * 点击省份节点时，该节点高亮显示并在中间展开下属所有城市卡片，地图定位至省地图中心（缩放级别为8级）
 * 点击直辖市节点时，该节点高亮显示，并在中间展开城市卡片，地图定位至直辖市中心（缩放级别为12级）
 */
const selectProvince = (province) => {
  // 设置高亮节点
  highlightedNode.value = province
  
  // 发送省份选择事件，用于更新中间城市卡片列表
  emit('province-select', province)
  
  // 根据节点类型执行不同操作
  if (province.isMunicipality) {
    // 直辖市：在地图上定位到市中心，缩放级别为12级
    emit('map-navigate', {
      center: province.center,
      zoom: province.zoom
    })
  } else {
    // 普通省份：加载城市数据用于其他用途，并在地图上定位到省份中心，缩放级别为8级
    loadCitiesByProvince(province.id)
      .then(cities => {
        console.log(`加载${province.name}的城市数据:`, cities);
      })
      .catch(error => {
        console.error(`加载${province.name}的城市数据失败:`, error);
      });
    
    // 发送地图定位事件，缩放级别为8级
    emit('map-navigate', {
      center: province.center,
      zoom: province.zoom
    })
  }
}
</script>

<style scoped>
.tree-menu {
  width: 100%;
  height: 100%;
  overflow-y: auto;
  padding: 0.5rem; /* 减小内边距 */
  box-sizing: border-box;
}

.tree-root {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.tree-node {
  margin: 0;
  padding: 0;
}

.node-content {
  display: flex;
  align-items: center;
  padding: 0.75rem; /* 增加内边距提高可点击区域和可读性 */
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.3s ease;
  margin-bottom: 2px; /* 添加节点间距 */
}

.node-content:hover {
  background-color: #e9ecef;
}

.node-content.highlighted {
  background-color: #007bff;
}

.node-toggle {
  width: 20px;
  text-align: center;
  margin-right: 8px; /* 增加右边距 */
  font-size: 0.8rem;
}

.node-label {
  flex: 1;
  font-weight: normal;
  color: #333;
  font-size: 0.95rem; /* 稍微增大字体 */
}

.node-content.highlighted .node-label {
  color: white;
}

.region-node > .node-content {
  background-color: #f8f9fa;
  font-weight: bold;
  border: 1px solid #dee2e6;
  padding: 0.5rem; /* 减小大区节点的内边距以适应更窄的侧边栏 */
  margin-top: 0.25rem;
  margin-bottom: 0.25rem;
}

.region-label {
  color: #495057;
  font-size: 0.9rem; /* 稍微减小大区标签字体 */
  white-space: nowrap; /* 防止换行 */
  overflow: hidden; /* 隐藏溢出文本 */
  text-overflow: ellipsis; /* 文本溢出时显示省略号 */
}

.node-content.highlighted .region-label {
  color: #003366; /* 使用深蓝色而非白色，确保在高亮状态下仍然可见 */
}

.province-node > .node-content {
  padding: 0.3rem 0.5rem 0.3rem 1.2rem; /* 调整省份节点内边距 */
}

.province-label {
  color: #6c757d;
  white-space: nowrap; /* 防止换行 */
  overflow: hidden; /* 隐藏溢出文本 */
  text-overflow: ellipsis; /* 文本溢出时显示省略号 */
}

.node-content.highlighted .province-label {
  color: white;
}

.children {
  list-style-type: none;
  padding: 0;
  margin: 0;
  padding-left: 0.8rem; /* 减小子节点整体缩进 */
}

.children .tree-node {
  border-left: 2px solid #dee2e6;
  margin-left: 8px;
  margin-top: 2px;
  margin-bottom: 2px;
}

.tree-node .node-content {
  cursor: pointer;
  transition: background-color 0.2s ease;
  border-radius: 4px;
  padding: 0.3rem 0.5rem; /* 调整节点内边距 */
  display: flex;
  align-items: center;
}

.tree-node .node-content:hover {
  background-color: #e9ecef;
}

.tree-node .node-content.highlighted {
  background-color: #007bff;
}
</style>

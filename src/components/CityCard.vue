<template>
  <div 
    class="city-card-container"
    @mouseenter="handleShowTooltip"
    @mouseleave="handleHideTooltip"
    ref="cardElement"
  >
    <div 
      class="city-card" 
      @click="handleCardClick"
    >
      <!-- 城市名称链接到百度百科 -->
      <h3 
        @click.stop="openBaiduBaike"
        :title="city.name"
      >
        {{ city.name }}
      </h3>
      
      <!-- 城市基本信息 - 按三行排列 -->
      <div class="city-info">
        <div class="info-row">
          <div class="info-item">
            <span class="info-label">人口：</span>
            <span class="info-value">{{ formatPopulation(city.population) }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">GDP：</span>
            <span class="info-value">{{ formatGDP(city.gdp) }}</span>
          </div>
        </div>
        <div class="info-row">
          <div class="info-item">
            <span class="info-label">可支配：</span>
            <span class="info-value" v-if="city.perCapitaDisposableIncome">{{ formatIncome(city.perCapitaDisposableIncome) }}</span>
            <span class="info-value info-unknown" v-else>未知</span>
          </div>
          <div class="info-item">
            <span class="info-label">房价：</span>
            <span class="info-value" v-if="city.averageHousePrice">{{ formatHousePrice(city.averageHousePrice) }}</span>
            <span class="info-value info-unknown" v-else>未知</span>
          </div>
        </div>
        <div class="info-row">
          <div class="info-item">
            <span class="info-label">车牌号：</span>
            <span class="info-value">{{ city.licensePlate || '未知' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">身份证：</span>
            <span class="info-value">{{ city.idPrefix || '未知' }}</span>
          </div>
        </div>
      </div>
      
      <!-- 操作按钮 -->
      <div class="actions" v-if="showActions">
        <button 
          @click.stop="toggleVisited"
          :class="{ active: isVisited }"
          class="action-btn"
        >
          {{ isVisited ? '已去过' : '去过' }}
        </button>
        <button 
          @click.stop="toggleCollected"
          :class="{ active: isCollected }"
          class="action-btn"
        >
          {{ isCollected ? '已收藏' : '收藏' }}
        </button>
        <button 
          @click.stop="toggleRan"
          :class="{ active: isRan }"
          class="action-btn"
        >
          {{ isRan ? '已跑过' : '跑过' }}
        </button>
      </div>
    </div>
    
    <!-- Tooltip内容现在动态创建，这里不需要再显示 -->
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { hasCityStatus, toggleCityStatus } from '../services/user-status'

const props = defineProps({
  city: {
    type: Object,
    required: true
  },
  showActions: {
    type: Boolean,
    default: false
  },
  position: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['card-click', 'select', 'status-change'])

// 使用城市唯一ID确保状态正确
const getUniqueCityId = computed(() => {
  // 如果城市对象已经有唯一ID（带省份前缀），直接使用
  if (props.city.id && props.city.id.includes('_')) {
    return props.city.id;
  }
  // 否则构造唯一ID（如果提供了provinceId）
  if (props.city.provinceId && props.city.originalId) {
    return `${props.city.provinceId}_${props.city.originalId}`;
  }
  // 最后回退到城市名称（可能不唯一）
  return props.city.name || props.city.id;
});

// 城市状态
const isVisited = ref(hasCityStatus(getUniqueCityId.value, 'visited'))
const isCollected = ref(hasCityStatus(getUniqueCityId.value, 'collected'))
const isRan = ref(hasCityStatus(getUniqueCityId.value, 'ran'))

// 监听城市ID变化，更新状态
watch(getUniqueCityId, (newId) => {
  isVisited.value = hasCityStatus(newId, 'visited')
  isCollected.value = hasCityStatus(newId, 'collected')
  isRan.value = hasCityStatus(newId, 'ran')
})

const showTooltip = ref(false)
const tooltipElement = ref(null)
const cardElement = ref(null)

// 切换去过状态
const toggleVisited = () => {
  toggleCityStatus(getUniqueCityId.value, 'visited')
  isVisited.value = !isVisited.value
  // 通知父组件状态已更改
  emit('status-change', { cityId: getUniqueCityId.value, type: 'visited', value: isVisited.value })
}

// 切换收藏状态
const toggleCollected = () => {
  toggleCityStatus(getUniqueCityId.value, 'collected')
  isCollected.value = !isCollected.value
  // 通知父组件状态已更改
  emit('status-change', { cityId: getUniqueCityId.value, type: 'collected', value: isCollected.value })
}

// 切换跑过状态
const toggleRan = () => {
  toggleCityStatus(getUniqueCityId.value, 'ran')
  isRan.value = !isRan.value
  // 通知父组件状态已更改
  emit('status-change', { cityId: getUniqueCityId.value, type: 'ran', value: isRan.value })
}

const handleCardClick = () => {
  // 可以在这里添加额外的点击处理逻辑
  emit('card-click', props.city);
  // 添加城市选择事件，用于地图联动
  emit('select', props.city);
}

// 显示tooltip
const handleShowTooltip = () => {
  console.log('Mouse entered card for city:', props.city.name);
  showTooltip.value = true;
  // 直接调用createTooltip而不是使用setTimeout
  createTooltip();
}

// 隐藏tooltip
const handleHideTooltip = () => {
  console.log('Mouse left card for city:', props.city.name);
  showTooltip.value = false;
  removeTooltip();
}

// 创建并添加tooltip到document.body
const createTooltip = () => {
  // 添加调试日志
  console.log('Creating tooltip for city:', props.city.name, 'Tags:', props.city.tags);
  
  // 检查是否有标签数据
  if (!props.city.tags || props.city.tags.length === 0) {
    console.log('No tags to display for city:', props.city.name);
    return;
  }
  
  // 移除已存在的tooltip
  removeTooltip();
  
  // 创建tooltip元素
  tooltipElement.value = document.createElement('div');
  tooltipElement.value.className = 'tags-tooltip';
  
  // 添加类名以应用正确的样式
  const tooltipClasses = ['tags-tooltip'];
  
  // 添加调试信息
  console.log('Position info for city:', props.city.name, props.position);
  
  // 简化判断逻辑，确保最左侧的卡片始终显示在右侧
  // 北京和上海等直辖市通常排在最前面，应该显示在右侧
  if (props.position.isLeftmost) {
    // 最左侧的卡片（包括北京、上海等）始终显示在右侧
    tooltipClasses.push('tooltip-right');
    console.log('Applying tooltip-right class for city:', props.city.name);
  } else if (props.position.isBottomRow && props.position.col < 2 && !props.position.isLeftmost) {
    // 最后一行的前两列但非最左侧的卡片显示在左上方
    // 添加 !props.position.isLeftmost 条件确保最左侧的卡片不会进入此分支
    tooltipClasses.push('tooltip-top-left');
    console.log('Applying tooltip-top-left class for city:', props.city.name);
  } else if (props.position.isBottomRow && props.position.isLeftmost) {
    // 最后一行最左侧的卡片显示在右上方
    tooltipClasses.push('tooltip-top-right');
    console.log('Applying tooltip-top-right class for city:', props.city.name);
  } else {
    // 默认显示在右侧
    tooltipClasses.push('tooltip-right');
    console.log('Applying default tooltip-right class for city:', props.city.name);
  }
  
  tooltipElement.value.className = tooltipClasses.join(' ');
  console.log('Final tooltip classes:', tooltipClasses);
  
  // 构建tooltip内容
  let tooltipContent = '';
  props.city.tags.forEach(tag => {
    tooltipContent += `<div class="tag-category">`;
    tooltipContent += `<div class="tag-category-title"><strong>${tag.type}</strong></div>`;
    tooltipContent += `<div class="tag-items">`;
    tag.items.forEach(item => {
      tooltipContent += `<span class="tag-item">${item}</span>`;
    });
    tooltipContent += `</div>`;
    tooltipContent += `</div>`;
  });
  tooltipElement.value.innerHTML = tooltipContent;
  
  // 设置样式确保可见
  tooltipElement.value.style.position = 'fixed';
  tooltipElement.value.style.zIndex = '999999';
  tooltipElement.value.style.backgroundColor = 'white';
  tooltipElement.value.style.border = '1px solid #ddd';
  tooltipElement.value.style.borderRadius = '6px';
  tooltipElement.value.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
  tooltipElement.value.style.padding = '12px';
  tooltipElement.value.style.width = '200px';
  tooltipElement.value.style.fontFamily = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif';
  tooltipElement.value.style.fontSize = '14px';
  
  // 添加标签内容的样式
  const style = document.createElement('style');
  style.innerHTML = `
    .tag-category {
      margin-bottom: 10px;
    }
    .tag-category:last-child {
      margin-bottom: 0;
    }
    .tag-category-title {
      margin-bottom: 4px;
      padding-bottom: 2px;
      border-bottom: 1px solid #eee;
    }
    .tag-category-title strong {
      color: #333;
      font-weight: 600;
    }
    .tag-items {
      display: flex;
      flex-wrap: wrap;
    }
    .tag-item {
      display: inline-block;
      background-color: #f5f5f5;
      color: #555;
      padding: 2px 6px;
      margin: 2px;
      border-radius: 3px;
      font-size: 13px;
    }
  `;
  tooltipElement.value.appendChild(style);
  
  // 根据类名设置不同的位置样式
  if (tooltipClasses.includes('tooltip-right')) {
    // 右侧显示样式
    tooltipElement.value.style.top = '';
    tooltipElement.value.style.left = '';
    tooltipElement.value.style.right = '';
    tooltipElement.value.style.bottom = '';
  } else if (tooltipClasses.includes('tooltip-top-left')) {
    // 左上方显示样式
    tooltipElement.value.style.top = '';
    tooltipElement.value.style.left = '';
    tooltipElement.value.style.right = '';
    tooltipElement.value.style.bottom = '';
  } else if (tooltipClasses.includes('tooltip-top-right')) {
    // 右上方显示样式
    tooltipElement.value.style.top = '';
    tooltipElement.value.style.left = '';
    tooltipElement.value.style.right = '';
    tooltipElement.value.style.bottom = '';
  }
  
  // 添加到document.body
  document.body.appendChild(tooltipElement.value);
  
  // 定位tooltip
  positionTooltip();
  
  console.log('Tooltip created and added to DOM');
}

// 定位tooltip
const positionTooltip = () => {
  if (!tooltipElement.value || !cardElement.value) {
    console.log('Cannot position tooltip: missing element references');
    return;
  }
  
  const cardRect = cardElement.value.getBoundingClientRect();
  console.log('Card position:', cardRect);
  
  // 获取当前应用的类名
  const classes = tooltipElement.value.className.split(' ');
  console.log('Tooltip classes for positioning:', classes);
  
  // 根据类名设置tooltip位置
  if (classes.includes('tooltip-top-left')) {
    // 左上方显示
    tooltipElement.value.style.top = `${cardRect.top - tooltipElement.value.offsetHeight}px`;
    tooltipElement.value.style.left = `${cardRect.left - tooltipElement.value.offsetWidth - 10}px`;
    console.log('Positioning tooltip top-left');
  } else if (classes.includes('tooltip-top-right')) {
    // 右上方显示
    tooltipElement.value.style.top = `${cardRect.top}px`;
    tooltipElement.value.style.left = `${cardRect.right + 10}px`;
    console.log('Positioning tooltip top-right');
  } else {
    // 右侧显示（默认）
    tooltipElement.value.style.top = `${cardRect.top}px`;
    tooltipElement.value.style.left = `${cardRect.right + 10}px`;
    console.log('Positioning tooltip right (default)');
  }
  
  // 确保tooltip在视口内
  const tooltipRect = tooltipElement.value.getBoundingClientRect();
  console.log('Tooltip position:', tooltipRect);
  
  if (tooltipRect.right > window.innerWidth) {
    tooltipElement.value.style.left = `${cardRect.left - tooltipElement.value.offsetWidth - 10}px`;
  }
  
  if (tooltipRect.bottom > window.innerHeight) {
    tooltipElement.value.style.top = `${window.innerHeight - tooltipElement.value.offsetHeight - 10}px`;
  }
  
  if (tooltipRect.top < 0) {
    tooltipElement.value.style.top = '10px';
  }
}

// 移除tooltip
const removeTooltip = () => {
  if (tooltipElement.value) {
    document.body.removeChild(tooltipElement.value)
    tooltipElement.value = null
  }
}

// 格式化人口数据（单位：万人，保留整数）
const formatPopulation = (population) => {
  if (!population) return '0w'
  const inTenThousand = population / 10000
  return `${Math.round(inTenThousand)}w`
}

// 格式化GDP数据（单位：万元，保留1位小数）
const formatGDP = (gdp) => {
  if (!gdp) return '0.0w'
  const inTenThousand = gdp / 10000
  return `${inTenThousand.toFixed(1)}w`
}

// 格式化人均可支配收入（单位：万元，保留1位小数）
const formatIncome = (income) => {
  if (!income) return '0.0w'
  const inTenThousand = income / 10000
  return `${inTenThousand.toFixed(1)}w`
}

// 格式化平均房价（单位：万元，保留1位小数）
const formatHousePrice = (price) => {
  if (!price) return '0.0w'
  const inTenThousand = price / 10000
  return `${inTenThousand.toFixed(1)}w/㎡`
}

// 打开百度百科链接
const openBaiduBaike = () => {
  const baikeUrl = `https://baike.baidu.com/item/${encodeURIComponent(props.city.name)}`
  window.open(baikeUrl, '_blank')
}

// 计算 tooltip 的位置样式
const tooltipStyle = computed(() => {
  const style = {}
  
  // 默认位置（右侧）
  style.top = '0px'
  style.left = '100%'
  style.marginLeft = '10px'
  style.marginRight = '0px'
  style.bottom = 'auto'
  
  // 如果是最左侧的卡片，将 tooltip 放在右侧
  if (props.position.isLeftmost) {
    // 保持默认位置（已经在右侧）
    return style
  }
  
  // 如果是最下一行的前两个卡片，将 tooltip 放在左上方
  if (props.position.isBottomRow) {
    // 第一个条件是确保是前两个卡片
    const cardsPerRow = Math.floor(document.querySelector('.card-container').clientWidth / 270) || 3
    if (props.position.index % cardsPerRow < 2) {
      style.top = 'auto'
      style.bottom = '0px'
      style.left = 'auto'
      style.right = '100%'
      style.marginLeft = '0px'
      style.marginRight = '10px'
    }
    
    // 如果是最下一行最左侧的卡片，将 tooltip 放在右上方
    if (props.position.isLeftmost && props.position.isBottomRow) {
      style.top = '0px'
      style.bottom = 'auto'
      style.left = '100%'
      style.right = 'auto'
      style.marginLeft = '10px'
      style.marginRight = '0px'
    }
  }
  
  return style
})

// 计算 tooltip 箭头的位置样式
const arrowStyle = computed(() => {
  const style = {}
  
  // 默认箭头位置（左侧）
  style.top = '15px'
  style.left = '-11px'
  style.right = 'auto'
  style.borderTopColor = 'transparent'
  style.borderRightColor = '#ddd'
  style.borderBottomColor = 'transparent'
  style.borderLeftColor = 'transparent'
  
  // 如果是最下一行的前两个卡片，箭头在右下角
  if (props.position.isBottomRow) {
    const cardsPerRow = Math.floor(document.querySelector('.card-container').clientWidth / 270) || 3
    if (props.position.index % cardsPerRow < 2) {
      style.top = 'auto'
      style.bottom = '15px'
      style.left = 'auto'
      style.right = '-11px'
      style.borderTopColor = 'transparent'
      style.borderRightColor = 'transparent'
      style.borderBottomColor = 'transparent'
      style.borderLeftColor = '#ddd'
    }
    
    // 如果是最下一行最左侧的卡片，箭头在左上角
    if (props.position.isLeftmost && props.position.isBottomRow) {
      style.top = '15px'
      style.bottom = 'auto'
      style.left = '-11px'
      style.right = 'auto'
      style.borderTopColor = 'transparent'
      style.borderRightColor = '#ddd'
      style.borderBottomColor = 'transparent'
      style.borderLeftColor = 'transparent'
    }
  }
  
  return style
})

// 计算 tooltip 内部箭头的位置样式
const innerArrowStyle = computed(() => {
  const style = {}
  
  // 默认内部箭头位置（左侧）
  style.top = '16px'
  style.left = '-10px'
  style.right = 'auto'
  style.borderTopColor = 'transparent'
  style.borderRightColor = 'white'
  style.borderBottomColor = 'transparent'
  style.borderLeftColor = 'transparent'
  
  // 如果是最下一行的前两个卡片，内部箭头在右下角
  if (props.position.isBottomRow) {
    const cardsPerRow = Math.floor(document.querySelector('.card-container').clientWidth / 270) || 3
    if (props.position.index % cardsPerRow < 2) {
      style.top = 'auto'
      style.bottom = '16px'
      style.left = 'auto'
      style.right = '-10px'
      style.borderTopColor = 'transparent'
      style.borderRightColor = 'transparent'
      style.borderBottomColor = 'transparent'
      style.borderLeftColor = 'white'
    }
    
    // 如果是最下一行最左侧的卡片，内部箭头在左上角
    if (props.position.isLeftmost && props.position.isBottomRow) {
      style.top = '16px'
      style.bottom = 'auto'
      style.left = '-10px'
      style.right = 'auto'
      style.borderTopColor = 'transparent'
      style.borderRightColor = 'white'
      style.borderBottomColor = 'transparent'
      style.borderLeftColor = 'transparent'
    }
  }
  
  return style
})

// 组件卸载时清理tooltip
onUnmounted(() => {
  removeTooltip()
})
</script>

<style scoped>
.city-card-container {
  position: relative;
  display: inline-block;
}

.city-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.1);
  padding: 12px;
  margin: 5px;
  transition: all 0.3s ease;
  cursor: pointer;
  /* 设置固定宽度和高度 */
  width: 260px;
  height: 180px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  z-index: 1;
}

.city-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.city-card h3 {
  margin: 0 0 8px 0;
  color: #2c3e50;
  cursor: pointer;
  text-decoration: none;
  font-size: 1.3rem;
  font-weight: 600;
  text-align: center;
  padding-bottom: 5px;
  border-bottom: 1px solid #eee;
  white-space: normal;
  word-break: break-all;
  line-height: 1.3;
  display: -webkit-box;
  line-clamp: 2;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.city-card h3:hover {
  color: #3498db;
  text-decoration: underline;
}

.city-info {
  margin: 5px 0; /* 从8px减少到5px，为标题提供更多空间 */
  flex-grow: 1;
}

.info-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 6px;
}

.info-item {
  display: flex;
  flex: 1;
}

.info-label {
  font-weight: 600;
  color: #7f8c8d;
  font-size: 0.85rem;
  min-width: 50px;
}

.info-value {
  color: #2c3e50;
  font-size: 0.9rem;
  font-weight: 500;
}

.info-unknown {
  color: #95a5a6;
  font-style: italic;
}

.actions {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid #eee;
}

.action-btn {
  flex: 1;
  margin: 0 2px;
  padding: 6px 2px;
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  color: #495057;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
}

.action-btn:hover {
  background-color: #e9ecef;
  border-color: #adb5bd;
}

.action-btn.active {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
  font-weight: bold;
}

.action-btn:active {
  transform: scale(0.95);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .city-card {
    width: 100%;
    height: 170px;
    padding: 10px;
  }
  
  .city-info {
    margin: 6px 0;
  }
  
  .info-row {
    margin-bottom: 5px;
  }
  
  .info-label {
    font-size: 0.8rem;
    min-width: 45px;
  }
  
  .info-value {
    font-size: 0.85rem;
  }
  
  .city-card h3 {
    font-size: 1.2rem;
    margin: 0 0 6px 0;
  }
  
  .action-btn {
    padding: 4px 1px;
    font-size: 0.7rem;
  }
}
</style>
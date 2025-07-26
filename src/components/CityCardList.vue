<template>
  <div class="city-card-list" ref="cardListContainer">
    <!-- 调试信息 -->
    <div v-if="false" class="debug-info">
      Container Width: {{ containerWidth }}px
    </div>
    
    <div class="card-container" ref="cardContainer">
      <CityCard 
        v-for="(city, index) in displayedCities" 
        :key="index" 
        :city="city"
        :show-actions="true"
        :position="cardPositions.find(p => p.index === index) || {}"
        @select="selectCity"
        @card-click="selectCity"
        @status-change="handleStatusChange"
      />
    </div>
    
    <!-- 加载更多提示 -->
    <div v-if="hasMore && !loading" class="load-more" @click="loadMore">
      点击加载更多...
    </div>
    <div v-if="loading" class="loading">
      加载中...
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import CityCard from './CityCard.vue'

const props = defineProps({
  cities: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['city-select', 'city-status-change'])

const displayedCities = ref([])
const currentPage = ref(1)
const pageSize = ref(20) // 每页显示20个城市
const loading = ref(false)
const cardListContainer = ref(null)
const cardContainer = ref(null)
const containerWidth = ref(0)

// 计算是否还有更多数据
const hasMore = computed(() => {
  return props.cities.length > displayedCities.value.length
})

// 初始化显示的城市数据
const initializeCities = () => {
  displayedCities.value = props.cities.slice(0, pageSize.value)
  currentPage.value = 1
}

// 更新容器宽度
const updateContainerWidth = () => {
  if (cardContainer.value) {
    containerWidth.value = cardContainer.value.offsetWidth;
    console.log('Card Container Width:', containerWidth.value, 'px');
  }
}

// 计算卡片宽度
const calculateCardWidth = () => {
  updateContainerWidth();
  if (containerWidth.value > 0) {
    // 计算单个卡片的理论宽度
    const cardWidth = (containerWidth.value - 20) / 3; // 减去大概的gap
    console.log('Calculated Card Width:', cardWidth, 'px');
  }
}

// 加载更多城市数据
const loadMore = () => {
  if (loading.value || !hasMore.value) return
  
  loading.value = true
  // 模拟加载延迟
  setTimeout(() => {
    const start = currentPage.value * pageSize.value
    const end = start + pageSize.value
    const newCities = props.cities.slice(start, end)
    displayedCities.value = [...displayedCities.value, ...newCities]
    currentPage.value++
    loading.value = false
  }, 500)
}

// 滚动加载
const handleScroll = () => {
  if (!cardListContainer.value || loading.value || !hasMore.value) return
  
  const { scrollTop, scrollHeight, clientHeight } = cardListContainer.value
  // 当滚动到距离底部100px时自动加载更多
  if (scrollHeight - scrollTop - clientHeight < 100) {
    loadMore()
  }
}

const cardPositions = ref([])
const cardsPerRow = computed(() => {
  if (containerWidth.value === 0) return 3 // 默认每行3个卡片
  const cardWidth = 260 // 卡片宽度
  const gap = 10 // 间隙
  return Math.max(1, Math.floor((containerWidth.value + gap) / (cardWidth + gap)))
})

// 计算卡片位置信息
const calculateCardPositions = () => {
  nextTick(() => {
    if (!cardContainer.value) return
  
    const cards = cardContainer.value.querySelectorAll('.city-card-container')
    const positions = []
    
    // 获取容器的宽度以计算每行卡片数
    const containerWidth = cardContainer.value.clientWidth
    const cardWidth = 260 // 卡片宽度
    const gap = 10 // 间隙
    const cardsPerRow = Math.max(1, Math.floor((containerWidth + gap) / (cardWidth + gap)))
    
    cards.forEach((card, index) => {
      const rect = card.getBoundingClientRect()
      const containerRect = cardContainer.value.getBoundingClientRect()
      
      // 计算卡片在网格中的行列位置
      const row = Math.floor(index / cardsPerRow)
      const col = index % cardsPerRow
      
      positions.push({
        index,
        top: rect.top - containerRect.top,
        left: rect.left - containerRect.left,
        row,
        col,
        isLeftmost: col === 0, // 最左侧的卡片
        isBottomRow: false // 先默认为false，后面再计算
      })
    })
    
    // 确定最下一行的卡片
    if (positions.length > 0) {
      // 找到最大行号
      const maxRow = Math.max(...positions.map(p => p.row))
      
      // 标记最下一行的卡片
      positions.forEach(position => {
        if (position.row === maxRow) {
          position.isBottomRow = true
        }
      })
    }
    
    cardPositions.value = positions
    
    // 添加调试信息
    console.log('Card positions calculated:', positions);
  })
}

const selectCity = (city) => {
  // 触发城市选择事件
  emit('city-select', city)
}

// 处理城市状态更改
const handleStatusChange = (statusData) => {
  // 将状态更改事件传递给父组件
  emit('city-status-change', statusData)
}

// 监听窗口大小变化
const handleResize = () => {
  if (cardListContainer.value) {
    containerWidth.value = cardListContainer.value.clientWidth
    calculateCardPositions()
  }
}

onMounted(() => {
  // 初始化容器宽度
  if (cardListContainer.value) {
    containerWidth.value = cardListContainer.value.clientWidth
  }
  
  // 添加窗口大小变化监听
  window.addEventListener('resize', handleResize)
  
  // 初始计算卡片位置
  setTimeout(calculateCardPositions, 100)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})

// 监听城市数据变化，重新计算位置
watch(() => props.cities, () => {
  initializeCities()
  nextTick(() => {
    calculateCardPositions()
  })
}, { immediate: true })

// 监听显示城市数据变化，重新计算位置
watch(displayedCities, () => {
  setTimeout(calculateCardPositions, 100)
})

// 初始化
initializeCities()
// 在组件挂载后立即计算卡片位置
calculateCardPositions()
</script>

<style scoped>
.card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: flex-start;
  padding-right: 5px; /* 为右侧tooltip预留的空间 */
}

.city-card-list {
  width: 100%;
  height: 100%;
  overflow-y: auto;
  background-color: #f5f5f5;
  padding: 8px; /* 调整内边距为8px */
  box-sizing: border-box;
  position: relative; /* 确保容器有定位上下文 */
  z-index: 1; /* 设置较低的z-index */
}

.city-card {
  flex: 0 0 260px; /* 固定宽度为260px */
  width: 260px; /* 固定宽度为260px */
  min-width: 260px; /* 最小宽度也为260px */
  max-width: 260px; /* 最大宽度也为260px */
  height: 170px; /* 固定高度 */
  box-sizing: border-box;
}

/* 响应式设计 - 保持固定每行3个卡片 */
@media (max-width: 1200px) {
  .city-card {
    flex: 0 0 260px;
    width: 260px;
    min-width: 260px;
    max-width: 260px;
    height: 170px;
  }
}

@media (max-width: 768px) {
  .city-card {
    flex: 0 0 calc(50% - 6px);
    width: calc(50% - 6px);
    min-width: 150px;
  }
}

@media (max-width: 480px) {
  .city-card {
    flex: 0 0 100%;
    width: 100%;
    min-width: auto;
  }
}

.load-more {
  text-align: center;
  padding: 1rem;
  background-color: #e9ecef;
  border-radius: 4px;
  cursor: pointer;
  margin: 1rem 0;
  width: 100%;
}

.load-more:hover {
  background-color: #dee2e6;
}

.loading {
  text-align: center;
  padding: 1rem;
  color: #666;
}
</style>
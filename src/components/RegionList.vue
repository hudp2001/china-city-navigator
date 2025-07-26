<template>
  <div class="region-list">
    <div v-for="region in regions" :key="region.name" class="region-item">
      <h3 @click="toggleRegion(region)">{{ region.name }}</h3>
      <div v-if="region.expanded" class="province-list">
        <div 
          v-for="province in region.provinces" 
          :key="province.name" 
          class="province-item"
          @click="selectProvince(province)"
        >
          {{ province.name }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const regions = ref([
  {
    name: '华东',
    expanded: false,
    provinces: [
      { name: '江苏省', cities: ['南京', '苏州', '无锡'] },
      { name: '浙江省', cities: ['杭州', '宁波', '温州'] },
      { name: '安徽省', cities: ['合肥', '芜湖', '蚌埠'] },
    ]
  },
  {
    name: '华北',
    expanded: false,
    provinces: [
      { name: '北京市', cities: ['北京'] },
      { name: '天津市', cities: ['天津'] },
      { name: '河北省', cities: ['石家庄', '唐山', '秦皇岛'] },
    ]
  }
])

const toggleRegion = (region) => {
  region.expanded = !region.expanded
}

const selectProvince = (province) => {
  console.log('选中省份:', province.name)
  // 这里可以触发地图定位或城市卡片更新
}
</script>

<style scoped>
.region-list {
  width: 100%;
  padding: 1rem;
  overflow-y: auto;
  background-color: #f5f5f5;
}

.region-item {
  margin-bottom: 1rem;
}

.region-item h3 {
  cursor: pointer;
  padding: 0.5rem;
  background-color: #e0e0e0;
  border-radius: 4px;
}

.province-list {
  margin-top: 0.5rem;
  padding-left: 1rem;
}

.province-item {
  cursor: pointer;
  padding: 0.5rem;
  margin: 0.25rem 0;
  background-color: #eeeeee;
  border-radius: 4px;
}

.province-item:hover {
  background-color: #e0e0e0;
}
</style>
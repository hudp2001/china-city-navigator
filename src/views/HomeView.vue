<template>
  <div class="home-view">
    <h1>欢迎来到中国省市百科导航</h1>
    <p>请选择左侧菜单中的地区查看详细信息</p>
  </div>
</template>

<script setup>
// 这个组件现在只作为占位符使用
// 所有主要布局组件都移到了MainLayout.vue中
</script>

<style scoped>
.home-view {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 2rem;
}

h1 {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #333;
}

p {
  font-size: 1.2rem;
  color: #666;
}
</style>
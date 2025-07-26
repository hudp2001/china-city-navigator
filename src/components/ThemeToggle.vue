<template>
  <div class="theme-toggle">
    <label class="switch">
      <input type="checkbox" v-model="isDarkMode" @change="toggleTheme" />
      <span class="slider"></span>
    </label>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const isDarkMode = ref(false)

const toggleTheme = () => {
  if (isDarkMode.value) {
    document.body.classList.add('dark-mode')
  } else {
    document.body.classList.remove('dark-mode')
  }
}
</script>

<style scoped>
.theme-toggle {
  position: fixed;
  top: 1rem;
  right: 2rem;
}
.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}
.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}
.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: 0.4s;
  border-radius: 34px;
}
.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: 0.4s;
  border-radius: 50%;
}
input:checked + .slider {
  background-color: #2196f3;
}
input:checked + .slider:before {
  transform: translateX(26px);
}
</style>
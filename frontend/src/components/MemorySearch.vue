<template>
  <div class="memory-search">
    <div class="search-box">
      <el-input
        v-model="searchQuery"
        placeholder="搜索记忆..."
        @keyup.enter="handleSearch"
        clearable
      />
      <el-button type="primary" @click="handleSearch">搜索</el-button>
      <el-button v-if="searchQuery" @click="clearSearch">清除</el-button>
    </div>

    <div class="filters">
      <div class="filter-item">
        <span>类别筛选：</span>
        <el-select v-model="category" placeholder="全部" @change="handleSearch" clearable>
          <el-option value="" label="全部" />
          <el-option v-for="cat in categories" :key="cat" :value="cat" :label="cat" />
        </el-select>
      </div>

      <div class="filter-item" v-if="isSearching">
        <span>相似度阈值：</span>
        <el-slider
          v-model="threshold"
          :min="0"
          :max="1"
          :step="0.01"
          :precision="2"
          @change="handleSearch"
          style="width: 200px;"
        />
        <span>{{ (threshold * 100).toFixed(0) }}%</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  categories: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['search'])

const searchQuery = ref('')
const category = ref('')
const threshold = ref(0.5)
const isSearching = ref(false)

const handleSearch = () => {
  isSearching.value = !!searchQuery.value
  emit('search', {
    query: searchQuery.value || null,
    category: category.value || null,
    threshold: threshold.value
  })
}

const clearSearch = () => {
  searchQuery.value = ''
  isSearching.value = false
  emit('search', {
    query: null,
    category: category.value || null,
    threshold: 0
  })
}
</script>

<style scoped>
.memory-search {
  margin-bottom: 20px;
}

.search-box {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.search-box .el-input {
  flex: 1;
}

.filters {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-item > span:first-child {
  white-space: nowrap;
}
</style>

<template>
  <div class="memory-search">
    <div class="search-card">
      <div class="search-box">
        <el-input
          v-model="searchQuery"
          placeholder="搜索内容..."
          @keyup.enter="handleSearch"
          clearable
          class="search-input"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-button type="primary" @click="handleSearch" class="search-btn">
          <el-icon><Search /></el-icon>
          搜索
        </el-button>
        <el-button v-if="searchQuery" @click="clearSearch" class="clear-btn">
          清除
        </el-button>
      </div>

      <div class="filters">
        <div class="filter-item metadata-filter">
          <span class="filter-label">
            <el-icon><Filter /></el-icon>
            元数据筛选
          </span>
          <div class="metadata-selects">
            <el-select v-model="selectedKey" placeholder="字段" @change="onKeyChange" clearable class="key-select">
              <el-option value="" label="全部" />
              <el-option v-for="key in metadataKeys" :key="key" :value="key" :label="key" />
            </el-select>
            <el-select 
              v-if="selectedKey" 
              v-model="selectedValue" 
              placeholder="值" 
              @change="handleSearch" 
              clearable 
              class="value-select"
            >
              <el-option value="" label="全部" />
              <el-option v-for="val in availableValues" :key="val" :value="val" :label="val" />
            </el-select>
          </div>
        </div>

        <div class="filter-item threshold-filter" v-if="isSearching">
          <span class="filter-label">
            <el-icon><Aim /></el-icon>
            相似度阈值
          </span>
          <el-slider
            v-model="threshold"
            :min="0"
            :max="1"
            :step="0.01"
            :precision="2"
            @change="handleSearch"
            class="threshold-slider"
          />
          <span class="threshold-value">{{ (threshold * 100).toFixed(0) }}%</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Search, Filter, Aim } from '@element-plus/icons-vue'

const props = defineProps({
  metadataKeys: {
    type: Array,
    default: () => []
  },
  metadataKeyValues: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['search'])

const searchQuery = ref('')
const selectedKey = ref('')
const selectedValue = ref('')
const threshold = ref(0.5)
const isSearching = ref(false)

// 根据选中的 key 获取可选值列表
const availableValues = computed(() => {
  if (!selectedKey.value || !props.metadataKeyValues[selectedKey.value]) {
    return []
  }
  return props.metadataKeyValues[selectedKey.value]
})

// 监听 key 变化时，更新可选值
const onKeyChange = () => {
  selectedValue.value = ''
  handleSearch()
}

const buildMetadataFilter = () => {
  if (!selectedKey.value || !selectedValue.value) {
    return null
  }
  return {
    [selectedKey.value]: selectedValue.value
  }
}

const handleSearch = () => {
  isSearching.value = !!searchQuery.value
  const metadata = buildMetadataFilter()
  emit('search', {
    query: searchQuery.value || null,
    metadata: metadata,
    threshold: threshold.value
  })
}

const clearSearch = () => {
  searchQuery.value = ''
  selectedKey.value = ''
  selectedValue.value = ''
  isSearching.value = false
  emit('search', {
    query: null,
    metadata: null,
    threshold: 0
  })
}
</script>

<style scoped>
.memory-search {
  margin-bottom: 24px;
}

.search-card {
  background: var(--bg-card);
  backdrop-filter: blur(10px);
  padding: 20px;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
  box-shadow: var(--shadow-card);
  transition: all 0.3s ease;
}

.search-card:hover {
  box-shadow: var(--shadow-md);
}

.search-box {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.search-input {
  flex: 1;
}

.search-btn {
  padding: 0 20px;
}

.search-btn .el-icon {
  margin-right: 4px;
}

.clear-btn {
  padding: 0 16px;
}

.filters {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
  align-items: center;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.metadata-filter .metadata-selects {
  display: flex;
  gap: 4px;
}

.metadata-filter .key-select,
.metadata-filter .value-select {
  width: 100px;
}

.threshold-filter {
  flex: 1;
  max-width: 320px;
}

.threshold-slider {
  flex: 1;
}

.threshold-value {
  min-width: 40px;
  text-align: right;
  font-size: 14px;
  font-weight: 600;
  color: var(--primary-color);
}
</style>

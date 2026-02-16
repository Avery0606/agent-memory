<template>
  <div class="memory-list" v-loading="loading">
    <el-empty v-if="!loading && memories.length === 0" description="暂无记忆" />

    <div v-else class="memory-items">
      <el-card
        v-for="item in memories"
        :key="item.id"
        class="memory-item"
      >
        <div class="memory-content">
          <div class="memory-text">{{ item.memory }}</div>
          <div class="memory-meta">
            <el-tag v-if="item.score" type="warning" size="small">
              相似度: {{ (item.score * 100).toFixed(1) }}%
            </el-tag>
            <el-tag v-if="item.metadata && item.metadata.category" type="primary" size="small">
              {{ item.metadata.category }}
            </el-tag>
            <span class="time">{{ formatTime(item.created_at) }}</span>
          </div>
        </div>

        <div class="memory-actions">
          <el-button size="small" type="primary" @click="startEdit(item)">编辑</el-button>
          <el-button size="small" type="danger" @click="confirmDelete(item.id)">删除</el-button>
        </div>

        <MemoryEdit
          v-if="editingId === item.id"
          :memory="item"
          @save="handleSave"
          @cancel="cancelEdit"
        />
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import MemoryEdit from './MemoryEdit.vue'
import { updateMemory, deleteMemory } from '../api'

defineProps({
  memories: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['refresh'])

const editingId = ref(null)

const formatTime = (timeStr) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  return date.toLocaleString('zh-CN')
}

const startEdit = (item) => {
  editingId.value = item.id
}

const cancelEdit = () => {
  editingId.value = null
}

const handleSave = async ({ memoryId, content }) => {
  try {
    await updateMemory(memoryId, content)
    editingId.value = null
    emit('refresh')
  } catch (error) {
    ElMessage.error('更新失败: ' + error.message)
  }
}

const confirmDelete = (memoryId) => {
  ElMessageBox.confirm('确定要删除这条记忆吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    handleDelete(memoryId)
  }).catch(() => {})
}

const handleDelete = async (memoryId) => {
  try {
    await deleteMemory(memoryId)
    emit('refresh')
  } catch (error) {
    ElMessage.error('删除失败: ' + error.message)
  }
}
</script>

<style scoped>
.memory-list {
  margin-top: 20px;
}

.memory-items {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.memory-item {
  margin-bottom: 0;
}

.memory-text {
  margin-bottom: 10px;
  line-height: 1.6;
}

.memory-meta {
  display: flex;
  gap: 10px;
  align-items: center;
  font-size: 12px;
  color: #909399;
  margin-bottom: 10px;
}

.memory-actions {
  display: flex;
  gap: 10px;
}
</style>

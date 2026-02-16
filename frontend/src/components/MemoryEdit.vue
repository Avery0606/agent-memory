<template>
  <div class="memory-edit">
    <el-input
      v-model="editContent"
      type="textarea"
      placeholder="编辑记忆内容..."
      :rows="4"
    />
    <div class="edit-actions">
      <el-button type="success" @click="saveEdit">保存</el-button>
      <el-button @click="cancelEdit">取消</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  memory: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['save', 'cancel'])

const editContent = ref('')

onMounted(() => {
  editContent.value = props.memory.memory || props.memory
})

const saveEdit = () => {
  emit('save', {
    memoryId: props.memory.id,
    content: editContent.value
  })
}

const cancelEdit = () => {
  emit('cancel')
}
</script>

<style scoped>
.memory-edit {
  margin-top: 10px;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 4px;
}

.edit-actions {
  margin-top: 10px;
  display: flex;
  gap: 10px;
}
</style>

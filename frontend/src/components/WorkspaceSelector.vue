<template>
  <div class="workspace-selector">
    <span>工作区：</span>
    <el-input
      v-model="workspace"
      placeholder="输入工作区名称"
      @keyup.enter="handleConfirm"
      style="width: 200px;"
    />
    <el-button type="primary" @click="handleConfirm" :disabled="!workspace">确定</el-button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const workspace = ref('default-workspace')

onMounted(() => {
  const saved = localStorage.getItem('lastWorkspace')
  if (saved) {
    workspace.value = saved
  }
  handleConfirm()
})

const handleConfirm = () => {
  if (!workspace.value) return
  localStorage.setItem('lastWorkspace', workspace.value)
  emit('update:workspace', workspace.value)
}

const emit = defineEmits(['update:workspace'])
</script>

<style scoped>
.workspace-selector {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.workspace-selector span {
  font-weight: bold;
}
</style>

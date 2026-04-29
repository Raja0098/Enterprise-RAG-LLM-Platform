<template>
  <transition name="toast-fade">
    <div v-if="visible" :class="['toast-box', typeClass]" role="alert">
      <div class="toast-content">
        <span v-if="title" class="font-bold mr-2">{{ title }}</span>
        <span>{{ message }}</span>
      </div>
      <button @click="visible = false" class="close-btn">×</button>
    </div>
  </transition>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

const props = defineProps({
  type: { type: String, default: 'info' }, // info | success | error | warning
  title: { type: String, default: '' },
  message: { type: String, required: true },
  duration: { type: Number, default: 3000 }
})

const visible = ref(true)

onMounted(() => {
  if (props.duration > 0) {
    setTimeout(() => { visible.value = false }, props.duration)
  }
})

const typeClass = computed(() => {
  const classes = {
    info: 'bg-blue-600 text-white',
    success: 'bg-emerald-600 text-white',
    error: 'bg-rose-600 text-white',
    warning: 'bg-amber-500 text-white'
  }
  return classes[props.type] || 'bg-slate-700 text-white'
})
</script>

<style scoped>
.toast-box {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  min-width: 300px;
  padding: 12px 20px;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.2);
  z-index: 9999;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.close-btn { background: none; border: none; color: white; font-size: 20px; cursor: pointer; opacity: 0.7; }
.close-btn:hover { opacity: 1; }

.toast-fade-enter-active, .toast-fade-leave-active { transition: all 0.4s ease; }
.toast-fade-enter-from { opacity: 0; transform: translate(-50%, -20px); }
.toast-fade-leave-to { opacity: 0; transform: translate(-50%, -20px); }
</style>
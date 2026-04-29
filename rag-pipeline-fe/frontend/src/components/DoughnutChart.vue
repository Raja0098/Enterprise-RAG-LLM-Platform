<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import { Chart, DoughnutController, ArcElement, Tooltip, Legend } from 'chart.js'

Chart.register(DoughnutController, ArcElement, Tooltip, Legend)

const props = defineProps({ data: Object })
const canvas = ref(null)
let chart = null

const initChart = () => {
  if (chart) chart.destroy()
  if (!canvas.value) return
  chart = new Chart(canvas.value, {
    type: 'doughnut',
    data: props.data,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: 'bottom', labels: { usePointStyle: true } } }
    }
  })
}

watch(() => props.data, initChart, { deep: true })
onMounted(initChart)
onBeforeUnmount(() => { if (chart) chart.destroy() })
</script>

<template>
  <div class="h-full w-full">
    <canvas ref="canvas"></canvas>
  </div>
</template>
<script setup>
import { ref, watch, onMounted, onBeforeUnmount, computed } from 'vue'
import { Chart, BarController, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from 'chart.js'

Chart.register(BarController, BarElement, CategoryScale, LinearScale, Tooltip, Legend)

const props = defineProps({
  data: { type: Object, default: () => ({ labels: [], datasets: [] }) }
})

const canvas = ref(null)
let chart = null

const createChart = () => {
  if (chart) chart.destroy()
  if (!canvas.value) return

  chart = new Chart(canvas.value.getContext('2d'), {
    type: 'bar',
    data: props.data,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, grid: { color: '#f1f5f9' } },
        x: { grid: { display: false } }
      }
    }
  })
}

watch(() => props.data, createChart, { deep: true })
onMounted(createChart)
onBeforeUnmount(() => { if (chart) chart.destroy() })
</script>

<template>
  <div class="h-full w-full">
    <canvas ref="canvas"></canvas>
  </div>
</template>
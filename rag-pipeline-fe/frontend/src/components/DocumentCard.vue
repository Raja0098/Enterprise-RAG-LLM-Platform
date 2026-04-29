<template>
  <div class="card-root">
    <div class="card-header">
      <div class="pill">{{ doc.name }}</div>
    </div>

    <div class="card-body">
      <div class="line">
        <span class="icon">📄</span>
        <div class="text small muted">Source Type: PDF Document</div>
      </div>

      <div class="line">
        <span class="icon">🧩</span>
        <div class="text small price">{{ doc.chunks || 0 }} <span class="muted">Chunks Embedded</span></div>
      </div>

      <div class="avail-row mt-3">
        <div class="avail-left">
          <div class="d-flex justify-content-between mb-1">
            <span class="small">Vector Store Sync:</span>
            <span class="small font-bold" :style="{ color: statusColor }">{{ doc.status || 'Active' }}</span>
          </div>
          <div class="progress-track">
            <div class="progress-fill" :style="{ width: '100%', backgroundColor: statusColor }"></div>
          </div>
        </div>
      </div>

      <div class="action mt-4">
        <button class="view-btn" @click="$emit('view', doc.id)">
          🔍 View Metadata
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({ doc: Object })
const statusColor = computed(() => props.doc.status === 'Processing' ? '#ffb400' : '#10b981')
</script>

<style scoped>
.card-root { width: 100%; max-width: 350px; background: white; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); overflow: hidden; border: 1px solid #f1f5f9; }
.card-header { padding: 15px; background: #f8fafc; display: flex; justify-content: center; }
.pill { background: #1e293b; color: white; padding: 10px 20px; border-radius: 12px; font-weight: 700; width: 100%; text-align: center; }
.card-body { padding: 20px; }
.line { display: flex; gap: 10px; align-items: center; margin-bottom: 12px; }
.progress-track { height: 6px; background: #e2e8f0; border-radius: 10px; overflow: hidden; }
.progress-fill { height: 100%; transition: width 0.5s ease; }
.view-btn { width: 100%; background: #f1f5f9; color: #1e293b; border: none; padding: 10px; border-radius: 10px; font-weight: 600; cursor: pointer; }
.view-btn:hover { background: #e2e8f0; }
</style>
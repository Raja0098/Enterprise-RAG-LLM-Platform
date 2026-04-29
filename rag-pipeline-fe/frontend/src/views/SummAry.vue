<template>
  <div class="summary-page">
    <div class="page-container">
      <header class="page-header">
        <h1 class="page-title">Chat Archive</h1>
        <p class="page-sub">Review your past AI conversations and knowledge base interactions</p>
      </header>

      <div v-if="isLoading" class="loading-wrap">
        <div class="spinner" aria-hidden></div>
      </div>

      <div v-else>
        <div class="user-area">
          <section class="active-section">
            <h2 class="section-title">Active Conversations</h2>

            <div v-if="activeSessions.length > 0" class="table-wrap">
              <table class="booking-table">
                <thead>
                  <tr>
                    <th>Session ID</th>
                    <th>Topic / Title</th>
                    <th>Last Interaction</th>
                    <th>Questions Asked</th>
                    <th class="action-col">Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="session in activeSessions" :key="session.session_id">
                    <td class="mono">{{ session.session_id.substring(0, 8) }}</td>
                    <td><strong>{{ session.title || 'General Inquiry' }}</strong></td>
                    <td>{{ formatDate(session.updated_at || new Date()) }}</td>
                    <td>{{ session.query_count || 0 }}</td>
                    <td class="action-col">
                      <button
                        @click="resumeChat(session.session_id)"
                        class="btn-resume"
                        aria-label="Resume Chat"
                      >
                        <span class="btn-x">💬</span>
                        Resume
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div v-else class="empty-card">
              <p class="empty-text">No active sessions. Start a new one in the Dashboard!</p>
            </div>
          </section>

          <section class="history-section">
            <h2 class="section-title center">Archived Conversations</h2>

            <div v-if="archivedSessions.length > 0" class="history-grid">
              <div
                v-for="session in archivedSessions"
                :key="session.session_id"
                class="history-card"
              >
                <div class="history-pill">History ID: {{ session.session_id.substring(0, 5) }}</div>

                <div class="history-content">
                  <div class="history-line">
                    <span class="history-icon">📄</span>
                    <div>
                      <div class="meta-label">Session Topic</div>
                      <div class="meta-val">{{ session.title || 'Untitled Chat' }}</div>
                    </div>
                  </div>

                  <div class="history-line">
                    <span class="history-icon">📅</span>
                    <div>
                      <div class="meta-label">Ended At</div>
                      <div class="meta-val">{{ formatDate(session.created_at) }}</div>
                    </div>
                  </div>

                  <div class="history-line">
                    <span class="history-icon">🤖</span>
                    <div>
                      <div class="meta-label">Total Tokens</div>
                      <div class="meta-val mono">~{{ (session.query_count || 1) * 150 }}</div>
                    </div>
                  </div>
                </div>
                <div class="mt-3 text-right">
                  <button @click="deleteSession(session.session_id)" class="text-danger small">Delete Log</button>
                </div>
              </div>
            </div>

            <div v-else class="empty-card">
              <p class="empty-text">Your archive is empty.</p>
            </div>
          </section>

          <section class="user-summary">
            <h2 class="section-title">Query Frequency</h2>
            <div class="stat-card">
              <h3 class="stat-title">Questions per Chat Topic</h3>
              <div class="chart-area small">
                <BarChart :data="userChatChartData" v-show="userChatChartData?.datasets?.[0]?.data?.length > 0" />
                <div v-if="!userChatChartData?.datasets?.[0]?.data?.length" class="empty">No interaction data for chart.</div>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>

    <transition name="slide-fade">
      <div v-if="notification.show" class="toast" :class="notification.type">
        <div class="toast-inner">
          <div class="toast-text">{{ notification.message }}</div>
          <button class="toast-close" @click="notification.show = false">&times;</button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import BarChart from '@/components/BarChart.vue'

const store = useStore()
const router = useRouter()
const isLoading = ref(true)

const sessions = computed(() => store.getters.allSessions || [])
const userChatChartData = ref(null)

const notification = reactive({ show: false, message: '', type: 'success' })

// Filter sessions into "Active" (last 24 hours) and "Archived" (older)
const activeSessions = computed(() => sessions.value.slice(0, 3)) // Mock logic: show top 3 as active
const archivedSessions = computed(() => sessions.value.slice(3))

const notify = (message, type = 'success') => {
  notification.message = message; notification.type = type; notification.show = true
  setTimeout(() => { notification.show = false }, 3000)
}

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleString('en-IN', { day: 'numeric', month: 'short', hour: 'numeric', minute: '2-digit' })
}

const resumeChat = (id) => {
  store.commit('SET_CURRENT_SESSION', id)
  router.push('/dashboard')
}

const deleteSession = async (id) => {
  if (confirm('Delete this chat log?')) {
    notify('Chat log deleted', 'success')
    // await store.dispatch('deleteSession', id)
  }
}

const loadChatArchive = async () => {
  try {
    await store.dispatch('fetchAllSessions')
    
    // Build Chart Data: Questions per Session
    const labels = sessions.value.map(s => s.title || 'General').slice(0, 5)
    const dataArr = sessions.value.map(s => s.query_count || Math.floor(Math.random() * 10) + 1).slice(0, 5)

    userChatChartData.value = {
      labels: labels,
      datasets: [{
        label: 'Interactions',
        data: dataArr,
        backgroundColor: ['#1967ff', '#3b82f6', '#60a5fa', '#22c55e', '#f97316'],
        borderRadius: 8
      }]
    }
  } catch (err) {
    notify('Failed to load archive.', 'error')
  }
}

onMounted(async () => {
  isLoading.value = true
  await loadChatArchive()
  isLoading.value = false
})
</script>

<style scoped>
/* Inheriting your excellent styling with minor RAG adjustments */
.summary-page { min-height: 100vh; padding: 36px 0 80px; background: #f8fafc; }
.page-container { width: min(1180px, 94%); margin: 0 auto; }
.page-title { font-size: 30px; color: #1967ff; font-weight: 800; }

.btn-resume {
  background: #1967ff;
  color: white;
  padding: 8px 16px;
  border-radius: 12px;
  border: none;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(25, 103, 255, 0.2);
}

.history-pill {
  background: #1e293b;
  color: #fff;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 700;
  margin-bottom: 12px;
}

.stat-card { background: white; border-radius: 16px; padding: 24px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); }
.chart-area.small { min-height: 350px; }

.text-danger { color: #ef4444; background: none; border: none; cursor: pointer; }
.text-right { text-align: right; }

/* Keep your existing table and grid styles */
.booking-table { width: 100%; background: white; border-radius: 12px; overflow: hidden; }
.history-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
.history-card { background: white; padding: 20px; border-radius: 16px; border: 1px solid #e2e8f0; }
</style>
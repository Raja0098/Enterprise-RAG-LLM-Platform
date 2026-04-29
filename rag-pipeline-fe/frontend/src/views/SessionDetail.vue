<template>
  <div class="booking-wrapper">
    <div class="booking-card">
      <div class="card-header">
        <div class="pill">Session ID: {{ sessionId.substring(0, 8) }}...</div>
      </div>

      <div class="card-body">
        <h2 class="title">Chat Settings</h2>
        <p class="subtitle">Update the title of your conversation for better organization</p>

        <form @submit.prevent="handleUpdate" class="booking-form">
          <label class="label">Chat Session Title</label>
          <input
            v-model="sessionTitle"
            class="input"
            required
            placeholder="e.g. Financial Report Analysis"
          />

          <div class="action">
            <button type="submit" class="book-btn" :disabled="loading">
              <span class="picon">📝</span> 
              {{ loading ? 'Saving...' : 'Update Title' }}
            </button>
          </div>
        </form>
      </div>
      
      <div class="card-footer text-center pb-4">
        <button class="btn-link" @click="router.push('/dashboard')">Back to Chat</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStore } from 'vuex'
import axios from 'axios'

const sessionTitle = ref('')
const loading = ref(false)
const route = useRoute()
const router = useRouter()
const store = useStore()

const sessionId = route.params.id // This comes from the URL /session/:id

const handleUpdate = async () => {
  loading.value = true
  try {
    // We call the FastAPI backend to update the session title
    // Note: You may need to add this PUT route to your FastAPI backend
    await axios.put(`http://localhost:8000/sessions/${sessionId}`, {
      title: sessionTitle.value
    })
    
    // Refresh sessions in store and go back to history
    await store.dispatch('fetchAllSessions')
    router.push('/summary')
  } catch (err) {
    console.error(err)
    alert('Failed to update session title')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  // If we had a way to fetch the current title, we'd do it here
  sessionTitle.value = "New Chat" 
})
</script>

<style scoped>
.booking-wrapper {
  min-height: 100vh;
  background: transparent;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 20px;
  font-family: Inter, sans-serif;
}

.booking-card {
  width: 100%;
  max-width: 450px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.pill {
  background: #1967ff; /* Changed from green to AI Blue */
  color: #fff;
  padding: 12px;
  border-radius: 12px;
  font-weight: 700;
  width: 90%;
  text-align: center;
}

.title {
  font-size: 24px;
  font-weight: 800;
  color: #1e293b;
  text-align: center;
}

.subtitle {
  text-align: center;
  color: #64748b;
  font-size: 14px;
}

.label {
  color: #475569;
  font-weight: 600;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.input {
  width: 100%;
  padding: 12px;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  background: white;
  transition: all 0.3s ease;
}

.input:focus {
  border-color: #1967ff;
  box-shadow: 0 0 0 4px rgba(25, 103, 255, 0.1);
}

.book-btn {
  width: 100%;
  padding: 14px;
  border-radius: 12px;
  background: #1e293b; /* Dark professional look */
  color: white;
  border: none;
  font-weight: 700;
  cursor: pointer;
  transition: 0.3s;
}

.book-btn:hover:not(:disabled) {
  background: #0f172a;
  transform: translateY(-2px);
}

.book-btn:disabled {
  opacity: 0.6;
}

.btn-link {
  background: none;
  border: none;
  color: #64748b;
  text-decoration: underline;
  cursor: pointer;
  font-size: 14px;
}
</style>
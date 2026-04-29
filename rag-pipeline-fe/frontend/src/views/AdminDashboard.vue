<template>
  <div class="min-h-screen py-6 px-4 bg-light admin-bg">
    <div class="container mx-auto">
      
      <div class="d-flex justify-content-between align-items-center mb-8">
        <h1 class="text-4xl font-bold text-primary m-0">RAG Control Center</h1>
        <div class="d-flex gap-3">
          <div class="stat-card">
            <small>Total Queries</small>
            <div>{{ stats.length ? stats.reduce((a, b) => a + b.count, 0) : 0 }}</div>
          </div>
          <div class="stat-card">
            <small>Docs Ingested</small>
            <div>{{ documents.length }}</div>
          </div>
        </div>
      </div>

      <div class="card border-0 shadow-lg rounded-4 mb-6 p-4">
        <h2 class="title-pill mb-4">Ingest Knowledge Base (PDF)</h2>
        <div class="row align-items-center">
          <div class="col-md-8">
            <label class="form-label text-muted">Upload PDF for the RAG Pipeline to analyze</label>
            <div class="input-group">
              <input 
                type="file" 
                class="form-control rounded-4" 
                @change="onFileSelected" 
                accept=".pdf"
                :disabled="isIngesting"
              />
              <button 
                @click="uploadDoc" 
                class="btn btn-primary rounded-4 px-4 ms-2"
                :disabled="!selectedFile || isIngesting"
              >
                <span v-if="isIngesting" class="spinner-border spinner-border-sm me-2"></span>
                {{ isIngesting ? 'Ingesting...' : '+ Upload & Process' }}
              </button>
            </div>
          </div>
          <div class="col-md-4">
            <div class="ingestion-alert p-3 rounded-4" v-if="isIngesting">
              <small>⚙️ Extracting text and generating embeddings...</small>
            </div>
          </div>
        </div>
      </div>

      <div class="row mb-6">
        <div class="col-md-12">
          <div class="card border-0 shadow-sm rounded-4 p-4">
            <h2 class="title-pill mb-4 bg-dark">Pipeline Configuration</h2>
            <div class="row g-3">
              <div class="col-md-6">
                <label class="form-label">LLM API Key (Gemini/OpenAI)</label>
                <div class="input-group">
                  <input 
                    v-model="apiKey" 
                    type="password" 
                    class="form-control rounded-4" 
                    placeholder="sk-xxxxxxxxxxxxxxxx" 
                  />
                  <button @click="saveSettings" class="btn btn-outline-dark rounded-4 ms-2">Save Key</button>
                </div>
              </div>
              <div class="col-md-6">
                <label class="form-label">RAG Model Temperature</label>
                <input type="range" class="form-range" min="0" max="1" step="0.1" v-model="temp">
                <div class="d-flex justify-content-between"><small>Precise</small><small>Creative</small></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <h2 class="mb-4 text-primary font-bold">Ingested Documents</h2>
      <div class="row">
        <div v-if="documents.length === 0" class="col-12 text-center py-5 text-muted">
          No documents found in the vector store.
        </div>

        <div v-for="doc in documents" :key="doc.id" class="col-md-6 col-lg-4 mb-5">
          <div class="card shadow-sm border-0 rounded-4 h-100 doc-card">
            <div class="card-body">
              <div class="mb-3">
                <span class="doc-pill">📄 {{ doc.name }}</span>
              </div>
              <p class="text-muted small">Ingested on: {{ doc.date }}</p>
              <div class="d-flex justify-content-between align-items-center">
                <span class="badge bg-light text-dark">{{ doc.chunks }} Chunks</span>
                <span class="text-success small">● Active</span>
              </div>
            </div>
            <div class="card-footer bg-transparent border-0 text-end">
              <button class="btn btn-outline-danger btn-sm" @click="deleteDoc(doc.id)">Remove</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'

const store = useStore()

// State from Vuex
const isIngesting = computed(() => store.getters.isIngesting)
const stats = computed(() => store.getters.chartData || [])

// Local State
const selectedFile = ref(null)
const apiKey = ref(localStorage.getItem('llm_api_key') || '')
const temp = ref(0.7)

// Mocked Document list (Ideally you'd fetch this from FastAPI)
const documents = ref([
  { id: 1, name: 'Company_Policy.pdf', date: '2026-04-20', chunks: 142 },
  { id: 2, name: 'Project_Specs.pdf', date: '2026-04-22', chunks: 85 }
])

const onFileSelected = (event) => {
  selectedFile.value = event.target.files[0]
}

const uploadDoc = async () => {
  if (!selectedFile.value) return
  try {
    await store.dispatch('uploadDocument', selectedFile.value)
    alert('Document ingested successfully into the vector database!')
    selectedFile.value = null
  } catch (err) {
    alert('Ingestion failed. Check backend logs.')
  }
}

const saveSettings = () => {
  store.dispatch('updateSettings', apiKey.value)
  alert('API Configuration updated.')
}

const deleteDoc = (id) => {
  if(confirm('Delete this from knowledge base?')) {
    documents.value = documents.value.filter(d => d.id !== id)
  }
}

onMounted(() => {
  store.dispatch('fetchAdminStats')
})
</script>

<style scoped>
.admin-bg {
  background: #f4f7fa; /* Cleaner background for admin */
  min-height: 100vh;
}

.title-pill {
  display: inline-block;
  background: #0d6efd;
  color: white;
  padding: 8px 18px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 10px;
}

.stat-card {
  background: white;
  padding: 10px 20px;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
  text-align: right;
}
.stat-card div { font-size: 24px; font-weight: 700; color: #0d6efd; }

.doc-pill {
  display: block;
  width: 100%;
  padding: 12px;
  border-radius: 10px;
  background: #eef2f7;
  color: #333;
  font-weight: 600;
  border-left: 4px solid #0d6efd;
}

.doc-card {
  transition: transform 0.2s;
  border: 1px solid #e0e6ed;
}
.doc-card:hover {
  transform: translateY(-5px);
}

.ingestion-alert {
  background: #fff3cd;
  border: 1px solid #ffeeba;
  color: #856404;
}

.bg-dark { background: #212529 !important; }
</style>
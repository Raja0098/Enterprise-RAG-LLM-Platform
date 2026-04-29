import { createStore } from 'vuex'
import axios from 'axios'

const ML_BASE = 'http://localhost:8000'

/** * GLOBAL AXIOS INTERCEPTOR
 * Automatically attaches the JWT token to every request 
 * so you don't have to write headers manually in every action.
 */
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Safe load from localStorage
let storedUser = null
try {
  const userString = localStorage.getItem('user')
  if (userString && userString !== 'undefined') {
    storedUser = JSON.parse(userString)
  }
} catch (e) {
  localStorage.removeItem('user')
}

export default createStore({
  state: {
    user: storedUser,
    token: localStorage.getItem('token') || null,
    
    // RAG & Chat State
    messages: [],
    sessions: [],
    currentSessionId: localStorage.getItem('current_session_id') || null,
    
    // Admin & ML State
    queryStats: [],
    allUsers: [],
    ingestionLoading: false,
    apiKey: localStorage.getItem('llm_api_key') || ''
  },

  mutations: {
    SET_USER(state, payload) {
      state.user = payload.user
      state.token = payload.token
      localStorage.setItem('user', JSON.stringify(payload.user))
      localStorage.setItem('token', payload.token)
    },
    LOGOUT(state) {
      state.user = null; state.token = null; state.currentSessionId = null
      localStorage.clear()
    },
    SET_MESSAGES(state, messages) { state.messages = messages },
    ADD_MESSAGE(state, msg) { state.messages.push(msg) },
    SET_SESSIONS(state, sessions) { state.sessions = sessions },
    SET_CURRENT_SESSION(state, id) {
      state.currentSessionId = id
      localStorage.setItem('current_session_id', id)
    },
    SET_STATS(state, stats) { state.queryStats = stats },
    SET_ALL_USERS(state, users) { state.allUsers = users },
    SET_INGESTION_STATUS(state, status) { state.ingestionLoading = status },
    SET_API_KEY(state, key) {
      state.apiKey = key
      localStorage.setItem('llm_api_key', key)
    }
  },

  actions: {
    // --- AUTH ---
    async login({ commit }, credentials) {
    const res = await axios.post(`${ML_BASE}/auth/login`, {
      username: credentials.username,
      password: credentials.password
    })

    const userPayload = {
      user: {
        id: res.data.user_id,
        username: credentials.username,
        is_admin: res.data.is_admin
      },
      token: res.data.access_token
    }

    commit('SET_USER', userPayload)
    return res
    } ,

    async register(_, payload) {
      return await axios.post(`${ML_BASE}/auth/register`, {
        username: payload.username,
        password: payload.password
      })
    },

    // --- RAG CHAT LOGIC ---
    async createNewSession({ commit }) {
      const res = await axios.post(`${ML_BASE}/chat/session`, { title: "New Chat" })
      commit('SET_CURRENT_SESSION', res.data.session_id)
      commit('SET_MESSAGES', [])
      return res.data.session_id
    },

    async askQuestion({ state, commit }, question) {
      // 1. Update UI with User Query
      commit('ADD_MESSAGE', { role: 'user', message: question })
      
      // 2. Persist User Question to DB
      await axios.post(`${ML_BASE}/chat/message`, {
        session_id: state.currentSessionId || 'default',
        role: 'user',
        response: question
      })

      // 3. Request RAG Pipeline Response
      const res = await axios.post(`${ML_BASE}/query`, {
        question: question,
        session_id: state.currentSessionId || 'default'
      })

      const aiMsg = {
        role: 'assistant',
        message: res.data.response,
        meta_data: res.data.meta_data || [],
        summary: res.data.summary || ""
      }

      // 4. Update UI with AI Response & Persist to DB
      commit('ADD_MESSAGE', aiMsg)
      await axios.post(`${ML_BASE}/chat/message`, {
        session_id: state.currentSessionId || 'default',
        role: 'assistant',
        response: res.data.response
      })
    },

    async fetchChatHistory({ commit }, sessionId) {
      const res = await axios.get(`${ML_BASE}/sessions/${sessionId}/chats`)
      // Mapping backend 'message' field to frontend property
      const history = res.data.chats.map(c => ({
        role: c.role,
        message: c.message,
        time: c.time
      }))
      commit('SET_MESSAGES', history)
    },

    async fetchAllSessions({ commit }) {
      const res = await axios.get(`${ML_BASE}/sessions`)
      commit('SET_SESSIONS', res.data)
    },

    async updateSessionTitle({ dispatch }, { sessionId, title }) {
      await axios.put(`${ML_BASE}/sessions/${sessionId}`, { title })
      await dispatch('fetchAllSessions')
    },

    // --- ADMIN & INGESTION ---
    async uploadDocument({ commit }, file) {
      commit('SET_INGESTION_STATUS', true)
      const formData = new FormData()
      formData.append('file', file)
      try {
        await axios.post(`${ML_BASE}/upload/`, formData)
      } finally {
        commit('SET_INGESTION_STATUS', false)
      }
    },

    async fetchAdminStats({ commit }) {
      const res = await axios.get(`${ML_BASE}/admin/stats`)
      commit('SET_STATS', res.data)
    },

    async fetchUsers({ commit }) {
      const res = await axios.get(`${ML_BASE}/users`)
      commit('SET_ALL_USERS', res.data)
    }
  },

  getters: {
    isAuthenticated: state => !!state.token,
    isAdmin: state => state.user?.is_admin,
    allMessages: state => state.messages,
    allSessions: state => state.sessions,
    allUsers: state => state.allUsers,
    isIngesting: state => state.ingestionLoading,
    chartData: state => state.queryStats
  }
})
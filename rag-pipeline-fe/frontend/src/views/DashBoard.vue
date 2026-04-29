<template>
  <div class="chat-container">

    <!-- HEADER -->
    <div class="chat-header">
      <h2 class="m-0 text-primary">RAG AI Assistant</h2>
      <button class="btn btn-outline-secondary btn-sm" @click="startNewChat">
        + New Chat
      </button>
    </div>

    <!-- CHAT AREA -->
    <div class="messages-area" ref="messageBox">

      <!-- EMPTY STATE -->
      <div v-if="messages.length === 0" class="welcome-screen">
        <div class="bot-icon">🤖</div>
        <h3>How can I help you today?</h3>
        <p>Ask anything about the uploaded documents.</p>

        <!-- 🔥 QUICK SUGGESTIONS -->
        <div class="suggestions">
          <button @click="handleFollowUp('Summarize the documents')">
            Summarize documents
          </button>
          <button @click="handleFollowUp('What topics are covered?')">
            What topics are covered?
          </button>
          <button @click="handleFollowUp('Give key insights')">
            Give key insights
          </button>
        </div>
      </div>

      <!-- MESSAGES -->
      <div 
        v-for="(msg, index) in messages" 
        :key="index" 
        :class="['message-wrapper', msg.role]"
      >
        <div class="message-bubble">

          <!-- TEXT -->
          <div class="content" v-html="formatMessage(msg.message)"></div>

          <!-- CITATIONS -->
          <div v-if="msg.meta_data && msg.meta_data.length" class="citations">
            <span class="source-label">Sources:</span>
            <span 
              v-for="(source, i) in msg.meta_data" 
              :key="i" 
              class="source-tag"
            >
              📄 {{ source.source || source }}
            </span>
          </div>

          <!-- 🔥 FOLLOW UPS -->
          <div 
            v-if="msg.role === 'assistant' && msg.follow_up && msg.follow_up.length"
            class="followups"
          >
            <button
              v-for="(f, i) in msg.follow_up"
              :key="i"
              class="followup-btn"
              @click="handleFollowUp(f.text || f)"
            >
              {{ f.text || f }}
            </button>
          </div>

        </div>
      </div>

      <!-- TYPING -->
      <div v-if="isTyping" class="message-wrapper assistant">
        <div class="message-bubble typing">
          <span class="dot"></span>
          <span class="dot"></span>
          <span class="dot"></span>
        </div>
      </div>

    </div>

    <!-- INPUT -->
    <div class="input-container">
      <div class="input-wrapper">
        <textarea
          v-model="userInput"
          @keydown.enter.prevent="handleSend"
          placeholder="Ask a question..."
          rows="1"
          ref="inputField"
          @input="adjustHeight"
        ></textarea>

        <button 
          class="send-btn" 
          :disabled="!userInput.trim() || isTyping"
          @click="handleSend"
        >
          <span v-if="!isTyping">➤</span>
          <span v-else class="spinner-border spinner-border-sm"></span>
        </button>
      </div>

      <p class="footer-text">
        Domain AI Assistant • RAG Pipeline
      </p>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onUpdated, nextTick, onMounted } from 'vue'
import { useStore } from 'vuex'

const store = useStore()

const userInput = ref('')
const isTyping = ref(false)
const messageBox = ref(null)
const inputField = ref(null)

const messages = computed(() => store.getters.allMessages)

onMounted(() => {
  scrollToBottom()
})

onUpdated(() => {
  scrollToBottom()
})

const scrollToBottom = () => {
  if (messageBox.value) {
    messageBox.value.scrollTop = messageBox.value.scrollHeight
  }
}

const handleSend = async () => {
  if (!userInput.value.trim() || isTyping.value) return

  const query = userInput.value
  userInput.value = ''
  resetInputHeight()

  isTyping.value = true

  try {
    await store.dispatch('askQuestion', query)
  } catch (error) {
    console.error("Chat Error:", error)
  } finally {
    isTyping.value = false
  }
}

/* 🔥 CLICKABLE FOLLOW-UP */
const handleFollowUp = async (text) => {
  if (isTyping.value) return

  userInput.value = text
  await handleSend()
}

/* 🔥 CHATGPT STYLE NEW CHAT */
const startNewChat = async () => {
  await store.dispatch('createNewSession')

  userInput.value = ''
  isTyping.value = false
}

/* FORMAT */
const formatMessage = (text) => {
  return text.replace(/\n/g, '<br>')
}

/* INPUT AUTO HEIGHT */
const adjustHeight = () => {
  const el = inputField.value
  el.style.height = 'auto'
  el.style.height = el.scrollHeight + 'px'
}

const resetInputHeight = () => {
  if (inputField.value) inputField.value.style.height = '45px'
}
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 85vh;
  max-width: 900px;
  margin: 20px auto;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  overflow: hidden;
}

.chat-header {
  padding: 15px 25px;
  background: #f8f9fa;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.messages-area {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background: #fdfdfd;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

/* WELCOME */
.welcome-screen {
  text-align: center;
  margin-top: 80px;
  color: #888;
}

.bot-icon {
  font-size: 50px;
  margin-bottom: 10px;
}

.suggestions {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  gap: 10px;
}

.suggestions button {
  padding: 8px 14px;
  border-radius: 20px;
  border: 1px solid #ddd;
  background: #f5f7ff;
  cursor: pointer;
  transition: 0.2s;
}

.suggestions button:hover {
  background: #e3ebff;
}

/* MESSAGE */
.message-wrapper {
  display: flex;
}

.message-wrapper.user {
  justify-content: flex-end;
}

.message-wrapper.assistant {
  justify-content: flex-start;
}

.message-bubble {
  max-width: 75%;
  padding: 12px 18px;
  border-radius: 18px;
}

.user .message-bubble {
  background: #007bff;
  color: white;
}

.assistant .message-bubble {
  background: #f1f0f0;
}

/* FOLLOWUPS */
.followups {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.followup-btn {
  background: #eef3ff;
  border: 1px solid #d0dcff;
  padding: 6px 12px;
  border-radius: 16px;
  font-size: 13px;
  cursor: pointer;
}

.followup-btn:hover {
  background: #dbe6ff;
}

/* INPUT */
.input-container {
  padding: 20px;
  border-top: 1px solid #eee;
}

.input-wrapper {
  display: flex;
  gap: 10px;
  background: #f8f9fa;
  padding: 10px 15px;
  border-radius: 24px;
}

textarea {
  flex: 1;
  border: none;
  background: transparent;
  outline: none;
  resize: none;
}

.send-btn {
  background: #007bff;
  color: white;
  border: none;
  width: 35px;
  height: 35px;
  border-radius: 50%;
}

.footer-text {
  text-align: center;
  font-size: 11px;
  color: #aaa;
  margin-top: 10px;
}
</style>
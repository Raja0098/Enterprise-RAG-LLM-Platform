<template>
  <div class="login-wrapper">
    <div class="login-card">
      <div class="card-header">
        <h2 class="title">Welcome To Your Personal ChatBOT</h2>
        <p class="subtitle">Please log in to continue</p>
      </div>

      <div class="card-body">
        <div v-if="error" class="error-box">{{ error }}</div>

        <form @submit.prevent="handleLogin" class="login-form">
          <label>Username</label>
          <input v-model="form.username" type="text" placeholder="Username or gmail"required />

          <label>Password</label>
          <input v-model="form.password" type="password" placeholder="*********"required />

          <button type="submit" class="btn-primary">
            <span class="btn-icon">🔑</span> Login
          </button>

        </form>

        <p class="footer-text">
          Don’t have an account?
          <router-link to="/register">Register</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

const form = reactive({ username: '', password: '' })
const error = ref(null)
const router = useRouter()
const store = useStore()

const handleLogin = async () => {
  error.value = null
  try {
    await store.dispatch('login', form)

    const user = store.state.user   // ✅ FIXED

    if (user && user.is_admin) {
      router.push('/admin/dashboard')
    } else if (user) {
      router.push('/dashboard')
    } else {
      error.value = 'Unexpected login issue.'
    }
  } catch (err) {
    error.value = err?.response?.data?.detail || 'Login failed.'
    console.error(err)
  }
}
</script>

<style scoped>
/* Center card within global background */
.login-wrapper {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center; /* centered vertically again */
  padding: 20px;
  box-sizing: border-box;
}

/* Compact card width */
.login-card {
  width: 100%;
  max-width: 420px; /* 👈 reduced width from 720px to 420px */
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  background: rgba(255, 255, 255, 0.97);
}

/* Blue header band */
.card-header {
  background-color: #1967ff;
  padding: 24px 16px;
  text-align: center;
}

.title {
  margin: 0;
  color: #fff;
  font-size: 22px;
  font-weight: 700;
}

.subtitle {
  margin: 6px 0 0;
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
}

/* Card body */
.card-body {
  padding: 28px 24px;
}

/* Form styling */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 8px;
  text-align: left;
}

.login-form label {
  font-size: 15px;
  color: #444;
  margin-top: 6px;
}

.login-form input {
  padding: 10px 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 15px;
  transition: box-shadow 0.2s, border-color 0.2s;
}

.login-form input:focus {
  border-color: #1967ff;
  box-shadow: 0 0 0 3px rgba(25, 103, 255, 0.1);
}

/* Login button */
.btn-primary {
  margin-top: 18px;
  background-color: #1967ff;
  color: white;
  border: none;
  padding: 10px;
  font-weight: 600;
  font-size: 15px;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.btn-primary:hover {
  background-color: #1259e2;
}

.btn-icon {
  font-weight: 700;
}

/* Error message box */
.error-box {
  background: #ffe0e0;
  color: #b10000;
  padding: 10px;
  border-radius: 6px;
  margin-bottom: 10px;
  font-size: 14px;
}

/* Footer text */
.footer-text {
  margin-top: 20px;
  font-size: 13px;
  text-align: center;
  color: #555;
}

.footer-text a {
  color: #1967ff;
  text-decoration: none;
  font-weight: 500;
}

.footer-text a:hover {
  text-decoration: underline;
}
</style>

<template>
  <div class="register-wrapper">
    <div class="register-card">
      <div class="card-header">
        <span class="header-icon">👤＋</span>
        <h2 class="title">Register</h2>
      </div>

      <div class="card-body">
        <p class="subtitle">Create Account</p>

        <div v-if="error" class="error-box">{{ error }}</div>

        <form @submit.prevent="handleRegister" class="register-form">
          <div class="grid-2">
            <div class="field">
              <label>Username <span class="required">*</span></label>
              <input v-model="form.username" type="text" required />
            </div>
            <div class="field">
              <label>Email <span class="required">*</span></label>
              <input v-model="form.email" type="email" placeholder="user@gmail.com" required />
            </div>
          </div>

          <div class="grid-2">
            <div class="field">
              <label>Password <span class="required">*</span></label>
              <input v-model="form.password" type="password" required />
            </div>
            <div class="field">
              <label>Confirm Password <span class="required">*</span></label>
              <input v-model="form.confirmPassword" type="password" required />
            </div>
          </div>

          <div class="grid-2">
            <div class="field">
              <label>Full Name</label>
              <input v-model="form.fullname" type="text" />
            </div>
            <div class="field">
              <label>Pin Code</label>
              <input
                v-model="form.pincode"
                type="text"
                maxlength="6"
                placeholder="6-digit PIN"
                pattern="[0-9]{6}"
              />
            </div>
          </div>

          <div class="field full-width">
            <label>Address</label>
            <textarea v-model="form.address" rows="3" placeholder="Full address"></textarea>
          </div>

          <button type="submit" class="btn-primary">
            <span class="btn-icon">👤</span> Register
          </button>
        </form>

        <p class="footer-text">
          Already have an account?
          <router-link to="/login">Login here</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

const form = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  fullname: '',
  address: '',
  pincode: ''
})

const error = ref(null)
const router = useRouter()
const store = useStore()

const handleRegister = async () => {
  error.value = null
  if (form.password !== form.confirmPassword) {
    error.value = 'Passwords do not match.'
    return
  }
  try {
    await store.dispatch('register', {
      username: form.username,
      email: form.email,
      password: form.password,
      address: form.address,
      pincode: form.pincode,
      fullname: form.fullname
    })
    router.push('/login')
  } catch (err) {
    error.value =
      'Registration failed. Please try again with a different username or check your inputs.'
    console.error(err)
  }
}
</script>

<style scoped>
/* ======== BASE FONT & LAYOUT ======== */
.register-wrapper {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 20px;
  box-sizing: border-box;
  font-family: "Inter", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  color: #222;
}

/* ======== CARD ======== */
.register-card {
  width: 100%;
  max-width: 720px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 20px 50px rgba(17, 24, 39, 0.12);
  background: rgba(255, 255, 255, 0.98);
}

/* ======== HEADER ======== */
.card-header {
  background-color: #1967ff;
  padding: 22px 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}
.header-icon {
  font-size: 28px;
  color: #fff;
}
.card-header .title {
  margin: 0;
  color: #fff;
  font-size: 24px;
  font-weight: 700;
  letter-spacing: 0.3px;
}

/* ======== BODY ======== */
.card-body {
  padding: 26px 36px;
  text-align: left;
}

/* ======== SUBTITLE ======== */
.subtitle {
  text-align: center;
  font-size: 16px;
  font-weight: 500;
  color: #1967ff;
  margin: 6px 0 20px;
}

/* ======== ERROR ======== */
.error-box {
  background: #fff0f0;
  color: #b10000;
  padding: 10px 12px;
  border-radius: 8px;
  margin-bottom: 14px;
  font-size: 14px;
  border: 1px solid #ffd6d6;
}

/* ======== GRID LAYOUT ======== */
.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin-bottom: 10px;
}

/* ======== FORM FIELDS ======== */
.field label {
  display: block;
  font-size: 14px;
  color: #333;
  margin-bottom: 6px;
  font-weight: 600;
}

.field input,
.field textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e3e7ee;
  border-radius: 8px;
  font-size: 15px;
  box-sizing: border-box;
  outline: none;
  transition: box-shadow 0.12s, border-color 0.12s;
}

.field input:focus,
.field textarea:focus {
  border-color: #1967ff;
  box-shadow: 0 0 0 3px rgba(25, 103, 255, 0.1);
}

/* ======== FULL WIDTH FIELD ======== */
.full-width {
  margin-top: 6px;
  margin-bottom: 12px;
}

/* ======== REQUIRED ======== */
.required {
  color: #d33;
  margin-left: 4px;
  font-weight: 700;
}

/* ======== BUTTON ======== */
.btn-primary {
  width: 100%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background-color: #1967ff;
  color: #fff;
  border: none;
  padding: 12px 16px;
  font-size: 16px;
  font-weight: 700;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s ease, transform 0.1s ease;
  margin-top: 10px;
  letter-spacing: 0.2px;
}

.btn-primary:hover {
  background-color: #155ed6;
  transform: translateY(-1px);
}

.btn-icon {
  font-size: 18px;
  color: inherit;
}

/* ======== FOOTER ======== */
.footer-text {
  margin-top: 14px;
  text-align: center;
  color: #666;
  font-size: 13.5px;
}
.footer-text a {
  color: #1967ff;
  font-weight: 600;
  text-decoration: none;
}
.footer-text a:hover {
  text-decoration: underline;
}

/* ======== RESPONSIVE ======== */
@media (max-width: 780px) {
  .grid-2 {
    grid-template-columns: 1fr;
  }
  .card-body {
    padding: 20px;
  }
  .register-card {
    max-width: 520px;
  }
  .card-header .title {
    font-size: 20px;
  }
}
</style>

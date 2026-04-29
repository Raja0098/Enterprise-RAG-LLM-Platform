<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4 shadow-sm">
    <div class="container-fluid">
      <a class="navbar-brand fw-bold text-primary" @click="goHome" style="cursor: pointer">
         KnowledgeAI
      </a>

      <div class="collapse navbar-collapse justify-content-center">
        <ul class="navbar-nav mb-2 mb-lg-0">
          <!-- <li class="nav-item">
            <router-link to="/dashboard" class="nav-link">Chat</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/summary" class="nav-link">History</router-link>
          </li> -->
          <li class="nav-item v-if='isAdmin'">
            <router-link to="/admin/dashboard" class="nav-link text-warning">ChatBot Dashboard</router-link>
          </li>
          <!-- <li class="nav-item v-if='isAdmin'">
            <router-link to="/admin/summary" class="nav-link">Analytics</router-link>
          </li> -->
          <!-- <li class="nav-item v-if='isAdmin'">
            <a class="nav-link" @click="openUserModal" style="cursor: pointer">Users</a>
          </li> -->
        </ul>
      </div>

      <div class="d-flex align-items-center">
        <span class="text-secondary me-3 small">Logged in as: <b>{{ user?.username }}</b></span>
        <button class="btn btn-outline-danger btn-sm rounded-pill px-3" @click="logout">Logout</button>
      </div>
    </div>
  </nav>

  <UserTable v-if="showUserModal" :modal="true" @close="closeUserModal" />
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { computed, ref } from 'vue'
import UserTable from '@/components/UserTable.vue'

const router = useRouter()
const store = useStore()
const showUserModal = ref(false)

const user = computed(() => store.getters.getUser)
const isAdmin = computed(() => store.getters.isAdmin)

const logout = () => { store.commit('LOGOUT'); router.push('/login') }
const goHome = () => router.push(isAdmin.value ? '/admin/dashboard' : '/dashboard')
const openUserModal = () => showUserModal.value = true
const closeUserModal = () => showUserModal.value = false
</script>
<template>
  <div :class="modal ? 'modal-overlay' : 'users-page'">
    <div class="content-wrap mx-auto">
      <h2 class="page-title">System User Management</h2>

      <div class="card shadow-lg border-0 rounded-4 overflow-hidden">
        <div class="table-responsive">
          <table class="table table-hover mb-0">
            <thead class="bg-slate">
              <tr>
                <th>ID</th>
                <th>Username</th>
                <th>Email</th>
                <th>Access Level</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in allUsers" :key="user.id">
                <td class="text-muted">#{{ user.id }}</td>
                <td class="fw-bold">{{ user.username }}</td>
                <td>{{ user.email }}</td>
                <td>
                  <span :class="user.is_admin ? 'badge bg-danger' : 'badge bg-primary'">
                    {{ user.is_admin ? 'Admin' : 'Standard' }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div v-if="modal" class="text-center mt-4">
        <button class="btn btn-secondary rounded-pill px-4" @click="$emit('close')">Close Manager</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useStore } from 'vuex'
const store = useStore()
const allUsers = computed(() => store.getters.allUsers)
onMounted(() => { if (!allUsers.value.length) store.dispatch('fetchUsers') })
</script>

<style scoped>
.modal-overlay { position: fixed; inset: 0; background: rgba(15, 23, 42, 0.9); z-index: 9999; display: flex; align-items: center; justify-content: center; padding: 20px; }
.bg-slate { background: #1e293b !important; color: white !important; }
.page-title { color: #1e293b; font-weight: 800; text-align: center; margin-bottom: 30px; }
.users-page { padding: 40px 20px; }
.content-wrap { width: 100%; max-width: 900px; }
.table th { border: none; padding: 15px; }
.table td { vertical-align: middle; padding: 15px; }
</style>
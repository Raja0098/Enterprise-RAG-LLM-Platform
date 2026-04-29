<!-- App.vue
<template>
  <div>
    <NavBar v-if="showNavbar" />
    <router-view />
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import NavBar from './components/NavBar.vue'

const route = useRoute()
const publicPages = ['/login', '/register']
const showNavbar = !publicPages.includes(route.path)
</script> -->
<!-- App.vue -->
<!-- App.vue -->
<!-- App.vue -->
<template>
  <div id="app">
    <NavBar v-if="showNavbar" />
    <router-view />
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { computed } from 'vue'
import NavBar from './components/NavBar.vue'

const route = useRoute()
const publicPages = ['/login', '/register', '/admin/login', '/admin/register']
const showNavbar = computed(() => !publicPages.includes(route.path))
</script>

<style>
/* Single global background for the whole app */
#app {
  min-height: 100vh;
  background-image: url('@/assets/parking-bg.jpg'); /* <-- put your image here */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed; /* optional */
}

/* Optional: ensure router-view content sits above background and gets some spacing */
router-view,
#app > * {
  position: relative;
  z-index: 1;
}
</style>

import { createRouter, createWebHistory } from 'vue-router'
import LogIn from '@/views/LogIn.vue'
import RegisTer from '@/views/RegisTer.vue'
import DashBoard from '@/views/DashBoard.vue' 
import SummAry from '@/views/SummAry.vue'     
import AdminDashboard from '../views/AdminDashboard.vue' 
import AdminSummary from '@/views/AdminSummary.vue'     
import UserTable from '../components/UserTable.vue'
// Import the session detail view we repurposed
import SessionDetail from '@/views/SessionDetail.vue' 
import store from '@/store'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'Login', component: LogIn },
  { path: '/register', name: 'Register', component: RegisTer },

  // User Routes
  { 
    path: '/dashboard', 
    name: 'Dashboard', 
    component: DashBoard, 
    meta: { requiresAuth: true } 
  },
  { 
    path: '/history', 
    name: 'Summary', 
    component: SummAry, 
    meta: { requiresAuth: true } 
  },
  // Added the Session Settings route
  { 
    path: '/session/settings/:id', 
    name: 'SessionDetail', 
    component: SessionDetail, 
    meta: { requiresAuth: true } 
  },

  // Admin Routes
  { 
    path: '/admin/dashboard', 
    name: 'AdminDashboard', 
    component: AdminDashboard, 
    meta: { requiresAdmin: true, requiresAuth: true } 
  },
  { 
    path: '/admin/analytics', 
    name: 'AdminSummary', 
    component: AdminSummary, 
    meta: { requiresAdmin: true, requiresAuth: true } 
  },
  { 
    path: '/admin/users', 
    name: 'UserTable', 
    component: UserTable, 
    meta: { requiresAdmin: true, requiresAuth: true } 
  },

  { path: '/:pathMatch(.*)*', redirect: '/login' },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = store.getters.isAuthenticated || !!localStorage.getItem('token');
  
  // Robust Admin Check
  let isAdmin = false;
  try {
    const user = JSON.parse(localStorage.getItem('user'));
    isAdmin = store.getters.isAdmin || (user && user.is_admin);
  } catch (e) {
    isAdmin = false;
  }

  // 1. Auth Guard
  if (to.meta.requiresAuth && !isAuthenticated) {
    return next({ name: 'Login' });
  }

  // 2. Admin Guard
  if (to.meta.requiresAdmin && !isAdmin) {
    return next({ name: 'Dashboard' });
  }

  next();
})

export default router
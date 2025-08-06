<script setup>
import { onMounted } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'
import { themeStore } from '@/stores/themeStore'
import RecentPosts from '@/components/RecentPosts.vue'
import Footer from '@/components/Footer.vue';

const auth = useAuthStore()

onMounted(() => {
  const saved = localStorage.getItem('theme')
  if (saved === 'dark') {
    themeStore.isDark = true
    document.documentElement.classList.add('dark')
  }
})
</script>

<template>
  <div class="min-h-screen flex flex-col bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100 transition-colors">
    <header class="bg-white dark:bg-gray-900 shadow p-4 flex justify-between items-center">
      <nav class="space-x-4">
        <RouterLink to="/" class="hover:underline">Inicio</RouterLink>
        <RouterLink v-if="auth.isLoggedIn" to="/new-post" class="hover:underline">Nuevo Post</RouterLink>
        <RouterLink v-if="!auth.isLoggedIn" to="/register" class="hover:underline">Registrarse</RouterLink>
        <RouterLink v-if="!auth.isLoggedIn" to="/login" class="hover:underline">Iniciar sesión</RouterLink>
        <button v-if="auth.isLoggedIn" @click="auth.logout" class="hover:underline">Cerrar sesión</button>
      </nav>
      <button @click="themeStore.toggleTheme()" class="flex items-center bg-gray-200 dark:bg-gray-700 p-2 rounded">
        <span v-if="themeStore.isDark">🌙 Dark</span>
        <span v-else>☀️ Light</span>
      </button>
    </header>

    <div class="flex-grow max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-4 gap-6 p-4">
      <!-- Main outlet -->
      <main class="lg:col-span-3">
        <RouterView />
      </main>

      <!-- Sidebar reciente -->
      <RecentPosts class="lg:col-span-1" />
    </div>
    
    <Footer />
  </div>
</template>
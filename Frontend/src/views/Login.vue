<template>
  <div class="max-w-md mx-auto bg-white dark:bg-gray-900 p-6 rounded-lg shadow-md">
    <h2 class="text-2xl font-semibold text-gray-800 dark:text-gray-100 mb-6">Accede a tu cuenta</h2>
    <form @submit.prevent="login" class="space-y-4">
      <div>
        <label for="username" class="block text-gray-700 dark:text-gray-300 font-medium mb-1">Usuario:</label>
        <input
          v-model="username"
          id="username"
          type="text"
          required
          class="w-full border border-gray-300 dark:border-gray-600 rounded-md p-2 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-400 transition-colors"
        />
      </div>
      <div>
        <label for="password" class="block text-gray-700 dark:text-gray-300 font-medium mb-1">Contraseña:</label>
        <input
          v-model="password"
          id="password"
          type="password"
          required
          class="w-full border border-gray-300 dark:border-gray-600 rounded-md p-2 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-400 transition-colors"
        />
      </div>
      <div v-if="error" class="bg-red-100 text-red-800 p-4 rounded-md mb-4">
        {{ error }}
      </div>
      <button
        type="submit"
        class="w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600 transition-colors"
      >
        Ingresar
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'

const username = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()
const auth = useAuthStore()

const API_URL = import.meta.env.VITE_API_URL

async function login() {
  try {
    const res = await fetch(`${API_URL}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username: username.value, password: password.value }),
    })

    if (!res.ok) {
      const { detail } = await res.json()
      throw new Error(detail || 'Error al iniciar sesión')
    }

    const data = await res.json()
    auth.login(data.access_token)
    router.push('/')
  } catch (err) {
    error.value = err.message
  }
}
</script>

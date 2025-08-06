<template>
  <div class="max-w-md mx-auto bg-white dark:bg-gray-900 p-6 rounded-lg shadow-md">
        <h2 class="text-2xl font-semibold text-gray-800 dark:text-gray-100 mb-6">Crea tu cuenta</h2>      
        <form @submit.prevent="register" class="space-y-4">
          <div>
            <label for="username" class="block text-gray-700 dark:text-gray-300 font-medium mb-1">Nombre de usuario:</label>
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
          <div v-if="success" class="bg-green-100 text-green-800 p-4 rounded-md mb-4">
            {{ success }}
          </div>
          <div v-if="error" class="bg-red-100 text-red-800 p-4 rounded-md mb-4">
            {{ error }}
          </div>  
          <button
            type="submit"
            class="w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600 transition-colors"
          >
            Registrarse
          </button>
        </form>
      </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const error = ref('')
const success = ref('')
const router = useRouter()

const API_URL = import.meta.env.VITE_API_URL

async function register() {
  try {
    const res = await fetch(`${API_URL}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: username.value, password: password.value }),
    })

    if (!res.ok) {
      const { detail } = await res.json()
      throw new Error(detail || 'Error al registrarse')
    }

    success.value = 'Usuario registrado. Redirigiendo al login...'
    error.value = ''
    setTimeout(() => router.push('/login'), 2000)
  } catch (err) {
    error.value = err.message
    success.value = ''
  }
}
</script>

<template>
  <div>
    <div v-if="post">
      <router-link to="/" class="text-sm text-blue-400 hover:underline">&larr; Volver al inicio</router-link>
      
      <div class="relative w-full h-64 mb-6 rounded-lg overflow-hidden shadow-lg">
        <img
          v-if="post.image_url"
          :src="post.image_url"
          alt="Imagen del post"
          class="object-cover w-full h-full"
        />
        <!-- Texto sobre la imagen -->
        <div class="absolute bottom-0 left-0 w-full p-4 bg-gradient-to-t from-black/60 to-transparent text-white">
          <h1 class="text-2xl font-bold">{{ post.title }}</h1>
          <p class="text-sm">Publicado el {{ new Date(post.created_at).toLocaleString() }}      - Autor {{ post.author }}</p>
        </div>
      </div>
      <div class="bg-white dark:bg-gray-900 p-4 rounded-lg shadow-md space-y-3">
        <QuillEditor 
          v-model:content="post.content"
          content-type="html"
          theme="bubble"
          read-only="true"
          class="bg-white text-gray-900"
        />
      </div>
      <button
        v-if="auth.isLoggedIn && post.author === authUser"
        @click="deletePost"
        style="margin-top: 1rem; background-color: crimson; color: white; padding: 0.5rem;"
      >
        Eliminar post
      </button>
    </div>
    <p v-else-if="error">{{ error }}</p>
    <p v-else>Cargando post...</p>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.bubble.css'
import { themeStore } from '@/stores/themeStore'

const auth = useAuthStore()
const authUser = ref('')

const route = useRoute()
const router = useRouter()
const post = ref(null)
const error = ref(null)

const fondo = computed(() => themeStore.isDark ? '#101828' : '#ffffff');
const texto = computed(() => themeStore.isDark ? '#f8fafc' : '#374151');
const placeholder = computed(() => themeStore.isDark ? '#d1d5dc' : '#6b7280');
const botones = computed(() => themeStore.isDark ? '#cbd5e1' : '#4b5563');
const botonActivoFondo = computed(() => themeStore.isDark ? '#1e293b' : '#dbeafe');
const botonActivoColor = computed(() => themeStore.isDark ? '#60a5fa' : '#2563eb');
const botonHoverFondo = computed(() => themeStore.isDark ? '#334155' : '#f3f4f6');

const API_URL = import.meta.env.VITE_API_URL

const fetchPost = async (id) => {
  if (auth.token) {
    try {
      const res = await fetch(`${API_URL}/me`, {
        headers: {
          Authorization: `Bearer ${auth.token}`
        }
      })
      const data = await res.json()
      authUser.value = data.usuario
    } catch {}
  }

  try {
    console.log('Parametros: ', route.params)
    const response = await fetch(`${API_URL}/posts/${id}`)
    if (!response.ok) throw new Error('Post no encontrado')
    post.value = await response.json()
  } catch (err) {
    error.value = err.message
  }
}

onMounted(async () => {
  fetchPost(route.params.id)
})

// Observar cambios en el parámetro de la ruta
watch(() => route.params.id, (newId) => {
  fetchPost(newId)
})

async function deletePost() {
  if (!confirm('¿Estás seguro de que deseas eliminar este post?')) return

  try {
    const res = await fetch(`${API_URL}/posts/${post.value._id}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${auth.token}`
      }
    })

    if (!res.ok) throw new Error('Error al eliminar el post')

    alert('Post eliminado')
    router.push('/')
  } catch (err) {
    alert('No se pudo eliminar: ' + err.message)
  }
}
</script>

<style scoped>
:deep(.ql-editor) {
  min-height: 15em;
  background-color: v-bind(fondo);
  color: v-bind(texto);
}

:deep(.ql-editor.ql-blank:before) {
  color: v-bind(placeholder);
  background-color: v-bind(fondo);
}

:deep(.ql-bubble .ql-picker){
  color: v-bind(placeholder);
  background-color: v-bind(fondo);
}

:deep(.ql-bubble .ql-fill){
  fill: v-bind(botones);
}

:deep(.ql-bubble .ql-stroke){
  stroke: v-bind(botones);
}

:deep(.ql-bubble.ql-toolbar button.ql-active, .ql-bubble .ql-toolbar button.ql-active, .ql-bubble.ql-toolbar .ql-picker-label.ql-active, .ql-bubble .ql-toolbar .ql-picker-label.ql-active, .ql-bubble.ql-toolbar .ql-picker-item.ql-selected, .ql-bubble .ql-toolbar .ql-picker-item.ql-selected){
  background-color: v-bind(botonActivoFondo);
  color: v-bind(botonActivoColor);
}

:deep(.ql-bubble.ql-toolbar button:hover:not(.ql-active), .ql-bubble .ql-toolbar button:hover:not(.ql-active)){
  background-color: v-bind(botonHoverFondo);
}
</style>
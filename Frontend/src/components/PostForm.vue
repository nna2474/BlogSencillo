<template>
  <div class="max-w-2xl mx-auto">
    <form @submit.prevent="handleSubmit" enctype="multipart/form-data" class="bg-white dark:bg-gray-900 p-6 rounded-lg shadow-md space-y-6 transition-colors">
      <h3 class="text-2xl font-semibold text-gray-800 dark:text-gray-100">Crear nuevo post</h3>
      
      <div>
        <label for="title" class="block text-gray-700 dark:text-gray-300 font-medium mb-1">Título:</label>
        <input v-model="title" id="title" required 
        class="w-full border border-gray-300 dark:border-gray-600 rounded-md p-2 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-400 transition-colors"/>
      </div>
      <div>
        <label class="block text-gray-700 dark:text-gray-300 font-medium mb-1">Contenido:</label>
        <div class="border border-gray-200 dark:border-gray-700 rounded-md">
          <QuillEditor 
            v-model:content="content"
            content-type="html"
            placeholder="Contenido del Post..."
            theme="snow"
            :toolbar="toolbar"
            class="bg-white text-gray-900"
          />
        </div>
      </div>
      <div>
  <label for="image" class="block text-gray-700 dark:text-gray-300 font-medium mb-1">Imagen destacada (opcional):</label>
  <div class="flex items-center space-x-4">
    <label for="image" class="cursor-pointer bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 px-4 py-2 rounded-md hover:bg-gray-300 dark:hover:bg-gray-600 transition">
      Seleccionar imagen
    </label>
    <span class="text-sm text-gray-600 dark:text-gray-400">
      {{ image ? image.name : 'No hay imagen seleccionada' }}
    </span>
    <input id="image" type="file" class="hidden" @change="handleFileChange" accept="image/*" />
  </div>
</div>
      <button type="submit" 
      class="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition">
        Publicar</button>
      <p v-if="message" class="text-center text-sm text-green-600 dark:text-green-400 mt-2">{{ message }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, emit } from 'vue'
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css'
import { useAuthStore } from '@/stores/useAuthStore'
import { themeStore } from '@/stores/themeStore'
import { recentPosts } from '@/stores/recentPosts'

const title = ref('')
const content = ref('')
const image = ref(null)
const message = ref('')
const auth = useAuthStore()

const fondo = computed(() => themeStore.isDark ? '#101828' : '#ffffff');
const texto = computed(() => themeStore.isDark ? '#f8fafc' : '#374151');
const placeholder = computed(() => themeStore.isDark ? '#d1d5dc' : '#6b7280');
const botones = computed(() => themeStore.isDark ? '#cbd5e1' : '#4b5563');
const botonActivoFondo = computed(() => themeStore.isDark ? '#1e293b' : '#dbeafe');
const botonActivoColor = computed(() => themeStore.isDark ? '#60a5fa' : '#2563eb');
const botonHoverFondo = computed(() => themeStore.isDark ? '#334155' : '#f3f4f6');

const API_URL = import.meta.env.VITE_API_URL

function handleFileChange(e) {
  image.value = e.target.files[0] || null
}

async function handleSubmit() {
  if (!auth.isLoggedIn) {
    message.value = 'Debes iniciar sesión para publicar.'
    return
  }

  const formData = new FormData()
  formData.append('title', title.value)
  formData.append('content', content.value)
  if (image.value) {
    formData.append('image', image.value)
  }

  try {
    const res = await fetch(`${API_URL}/posts`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${auth.token}`,
      },
      body: formData,
    })

    if (!res.ok) throw new Error('Error al publicar')
    const data = await res.json()
    message.value = 'Post publicado correctamente'
    title.value = ''
    content.value = ''
    image.value = null

    recentPosts.PostRecientes();
  } catch (err) {
    message.value = err.message
  }
}

const toolbar = [
    [{ header: [1, 2, 3, false] }],
    ['bold', 'italic', 'underline', 'strike'],
    [{ align: [] }],
    ['link', 'video'],
    [{ 'script': 'sub'}, { 'script': 'super' }],
    [{ 'indent': '-1'}, { 'indent': '+1' }],
    ['clean']
  ]
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

:deep(.ql-snow .ql-picker){
  color: v-bind(placeholder);
  background-color: v-bind(fondo);
}

:deep(.ql-snow .ql-fill){
  fill: v-bind(botones);
}

:deep(.ql-snow .ql-stroke){
  stroke: v-bind(botones);
}

:deep(.ql-snow.ql-toolbar button.ql-active, .ql-snow .ql-toolbar button.ql-active, .ql-snow.ql-toolbar .ql-picker-label.ql-active, .ql-snow .ql-toolbar .ql-picker-label.ql-active, .ql-snow.ql-toolbar .ql-picker-item.ql-selected, .ql-snow .ql-toolbar .ql-picker-item.ql-selected){
  background-color: v-bind(botonActivoFondo);
  color: v-bind(botonActivoColor);
}

:deep(.ql-snow.ql-toolbar button:hover:not(.ql-active), .ql-snow .ql-toolbar button:hover:not(.ql-active)){
  background-color: v-bind(botonHoverFondo);
}
</style>

<template>
  <div class="space-y-6">
    <h2 class="text-2xl font-semibold text-gray-800 dark:text-gray-100">Posts</h2>
    <div v-if="paginatedPosts.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="post in paginatedPosts"
        :key="post._id"
        class="bg-white dark:bg-gray-900 rounded-lg shadow-md overflow-hidden"
      >
        <router-link :to="`/post/${post._id}`" class="block">
          <div class="relative w-full h-48">
            <img
              v-if="post.image_url"
              :src="post.image_url"
              alt="Imagen del post"
              class="object-cover w-full h-full"
            />
            <div class="absolute bottom-0 left-0 w-full p-4 bg-gradient-to-t from-black/60 to-transparent text-white">
              <h3 class="text-lg font-semibold truncate">{{ post.title }}</h3>
              <small class="block">{{ new Date(post.created_at).toLocaleString() }}</small>
            </div>
          </div>
          <div class="p-4">
            <div class="text-gray-700 dark:text-gray-300 text-sm line-clamp-3" v-html="post.content"></div>
          </div>
        </router-link>
      </div>
    </div>
    <p v-else class="text-gray-700 dark:text-gray-300">Cargando posts...</p>

    <!-- Paginación -->
    <div v-if="totalPages > 1" class="flex justify-center space-x-2 mt-4">
      <button
        v-for="page in totalPages"
        :key="page"
        @click="currentPage = page"
        :class="[
          'px-4 py-2 rounded-md',
          page === currentPage
            ? 'bg-blue-500 text-white'
            : 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 hover:bg-gray-300 dark:hover:bg-gray-600'
        ]"
      >
        {{ page }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

const posts = ref([])
const currentPage = ref(1)
const postsPerPage = 9

const API_URL = import.meta.env.VITE_API_URL

onMounted(async () => {
  try {
    const response = await fetch(`${API_URL}/posts`)
    const data = await response.json()
    posts.value = data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
  } catch (error) {
    console.error('Error al cargar los posts:', error)
  }
})

const paginatedPosts = computed(() => {
  const start = (currentPage.value - 1) * postsPerPage
  const end = start + postsPerPage
  return posts.value.slice(start, end)
})

const totalPages = computed(() => Math.ceil(posts.value.length / postsPerPage))
</script>
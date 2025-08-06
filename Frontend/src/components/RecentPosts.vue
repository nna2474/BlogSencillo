<template>
  <aside class="bg-white dark:bg-gray-900 p-4 rounded-lg shadow-md space-y-3">
    <h4 class="text-lg font-semibold text-gray-800 dark:text-gray-100">Posts Recientes</h4>
    <ul class="text-sm text-gray-700 dark:text-gray-300 space-y-2">
      <li v-for="post in recentPosts.recent" :key="post._id">
        <RouterLink :to="`/post/${post._id}`" class="block rounded-lg overflow-hidden shadow-md">
          <div class="relative w-full h-32">
            <img
              v-if="post.image_url"
              :src="post.image_url"
              alt="Imagen del post"
              class="object-cover w-full h-full"
            />
            <div class="absolute bottom-0 left-0 w-full p-2 bg-gradient-to-t from-black/60 to-transparent text-white">
              <h5 class="text-sm font-semibold truncate">{{ post.title }}</h5>
            </div>
          </div>
        </RouterLink>
      </li>
    </ul>
  </aside>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { recentPosts } from '@/stores/recentPosts'

onMounted(async () => {
  await recentPosts.PostRecientes();
  console.log('Recent posts loaded:', recentPosts.recent);
})


</script>

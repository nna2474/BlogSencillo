<template>
  <div>
    <header class="relative">
      <div class="bg-white dark:bg-gray-900 overflow-hidden rounded-lg shadow-md space-y-3">
        <img
          src="@/assets/CabeceraBlog.png"
          alt="Cabecera del blog"
          class="w-full h-auto object-cover"
        />
      </div>
    </header>
    <main class="container mx-auto py-8">
      <BlogFeed />
    </main>
  </div>
</template>
<script setup>
import BlogFeed from '@/components/BlogFeed.vue'
</script>
<style scoped>h1 { color: #42b983; }</style>
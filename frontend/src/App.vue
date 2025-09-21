<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <!-- ヘッダー -->
    <header class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center">
            <router-link to="/" class="flex items-center">
              <h1 class="text-2xl font-bold text-gray-900">Stack Watcher</h1>
              <span class="ml-3 text-sm text-gray-500">統合監視ダッシュボード</span>
            </router-link>
          </div>
          
          <!-- ナビゲーション -->
          <nav class="flex items-center space-x-6">
            <router-link 
              to="/" 
              class="nav-link"
              :class="{ 'active': $route.name === 'Home' }"
            >
              ホーム
            </router-link>
            <router-link 
              to="/dashboard" 
              class="nav-link"
              :class="{ 'active': $route.name === 'Dashboard' }"
            >
              ダッシュボード
            </router-link>
            <router-link 
              to="/about" 
              class="nav-link"
              :class="{ 'active': $route.name === 'About' }"
            >
              このアプリについて
            </router-link>
          </nav>
        </div>
      </div>
    </header>

    <!-- メインコンテンツ -->
    <main class="flex-1">
      <router-view />
    </main>
  </div>
</template>

<script setup>
// ルーターベースのアプリケーション
</script>

<style scoped>
.nav-link {
  @apply px-3 py-2 rounded-md text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-100 transition-colors;
}

.nav-link.active {
  @apply bg-blue-100 text-blue-700;
}
</style>

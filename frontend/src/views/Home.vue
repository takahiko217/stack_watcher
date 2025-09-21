<template>
  <div class="home-page">
    <!-- ヒーローセクション -->
    <section class="hero-section">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 text-center">
        <h1 class="hero-title">
          Stack Watcher
        </h1>
        <p class="hero-subtitle">
          株価・指数・気象データの統合監視ダッシュボード
        </p>
        <p class="hero-description">
          リアルタイムで各種データを可視化し、トレンドを一目で把握できます
        </p>
        
        <!-- アクションボタン -->
        <div class="hero-actions">
          <router-link 
            to="/dashboard" 
            class="primary-button"
          >
            ダッシュボードを開く
          </router-link>
          
          <router-link 
            to="/about" 
            class="secondary-button"
          >
            詳細情報
          </router-link>
        </div>
      </div>
    </section>

    <!-- 機能紹介セクション -->
    <section class="features-section">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h2 class="section-title">主要機能</h2>
        
        <div class="features-grid">
          <!-- 株価監視 -->
          <div class="feature-card">
            <h3 class="feature-title">株価データ監視</h3>
            <p class="feature-description">
              主要銘柄の株価推移をリアルタイムで監視
            </p>
          </div>

          <!-- 指数監視 -->
          <div class="feature-card">
            <h3 class="feature-title">市場指数監視</h3>
            <p class="feature-description">
              日本の主要市場指数の動向を把握
            </p>
          </div>

          <!-- 気象データ -->
          <div class="feature-card">
            <h3 class="feature-title">気象データ連携</h3>
            <p class="feature-description">
              気象情報を統合し、市場への影響を分析
            </p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
// ホームページコンポーネント
</script>

<style scoped>
.home-page {
  @apply bg-white;
}

.hero-section {
  @apply bg-gradient-to-br from-blue-50 to-indigo-100;
}

.hero-title {
  @apply text-4xl md:text-6xl font-bold text-gray-900 mb-6;
}

.hero-subtitle {
  @apply text-xl md:text-2xl text-gray-700 mb-4;
}

.hero-description {
  @apply text-lg text-gray-600 mb-8 max-w-2xl mx-auto;
}

.hero-actions {
  @apply flex flex-col sm:flex-row gap-4 justify-center items-center;
}

.primary-button {
  @apply inline-flex items-center px-8 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors shadow-lg;
}

.secondary-button {
  @apply inline-flex items-center px-8 py-3 bg-white text-blue-600 font-semibold rounded-lg border-2 border-blue-600 hover:bg-blue-50 transition-colors;
}

.features-section {
  @apply bg-gray-50;
}

.section-title {
  @apply text-3xl font-bold text-gray-900 text-center mb-12;
}

.features-grid {
  @apply grid grid-cols-1 md:grid-cols-3 gap-8;
}

.feature-card {
  @apply bg-white rounded-lg p-6 shadow-sm border border-gray-200 hover:shadow-md transition-shadow;
}

.feature-title {
  @apply text-xl font-semibold text-gray-900 mb-3;
}

.feature-description {
  @apply text-gray-600 mb-4;
}
</style>

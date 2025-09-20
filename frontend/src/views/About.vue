<!-- 
  このアプリについてページコンポーネント
  
  アプリケーションの情報を表示するページです。
-->

<template>
  <div class="about">
    <h1>Stack Watcher について</h1>
    
    <!-- アプリケーション概要 -->
    <div class="app-info">
      <h2>🎯 アプリケーション概要</h2>
      <p>
        Stack Watcher は、現代的なWebアプリケーション開発のベストプラクティスを示すサンプルアプリケーションです。
        Vue.js をフロントエンド、FastAPI をバックエンドとして使用し、保守しやすい構造で設計されています。
      </p>
    </div>
    
    <!-- 技術スタック -->
    <div class="tech-stack">
      <h2>⚡ 使用技術</h2>
      <div class="tech-grid">
        <div class="tech-item">
          <h3>フロントエンド</h3>
          <ul>
            <li>Vue.js 3 - プログレッシブフレームワーク</li>
            <li>Vue Router - シングルページアプリケーション</li>
            <li>Pinia - 状態管理</li>
            <li>Vite - 高速ビルドツール</li>
          </ul>
        </div>
        <div class="tech-item">
          <h3>バックエンド</h3>
          <ul>
            <li>FastAPI - 高性能Webフレームワーク</li>
            <li>Python 3.11+ - プログラミング言語</li>
            <li>Uvicorn - ASGIサーバー</li>
            <li>SQLAlchemy - ORMライブラリ</li>
          </ul>
        </div>
      </div>
    </div>
    
    <!-- 特徴 -->
    <div class="features">
      <h2>✨ 特徴</h2>
      <div class="feature-list">
        <div class="feature-item">
          <h3>🔰 初心者フレンドリー</h3>
          <p>豊富なコメントと分かりやすい構造で、プログラミング初心者でも理解しやすく設計されています。</p>
        </div>
        <div class="feature-item">
          <h3>🏗️ モジュラー設計</h3>
          <p>機能ごとにモジュール化され、拡張性と保守性を重視した設計になっています。</p>
        </div>
        <div class="feature-item">
          <h3>📚 国際標準対応</h3>
          <p>ドキュメント管理やプロジェクト構造において国際標準に準拠しています。</p>
        </div>
        <div class="feature-item">
          <h3>🚀 最新技術</h3>
          <p>最新のフレームワークとツールを使用し、現代的な開発手法を採用しています。</p>
        </div>
      </div>
    </div>
    
    <!-- バージョン情報 -->
    <div class="version-info">
      <h2>📋 バージョン情報</h2>
      <div class="version-card">
        <p><strong>アプリケーションバージョン:</strong> 1.0.0</p>
        <p><strong>最終更新:</strong> {{ currentDate }}</p>
        <p><strong>開発者:</strong> Stack Watcher Team</p>
      </div>
    </div>
  </div>
</template>

<script>
/**
 * このアプリについてページコンポーネント
 * 
 * アプリケーションの詳細情報を表示します。
 */
import { ref, onMounted } from 'vue'

export default {
  name: 'About',
  
  setup() {
    // 現在の日付を表示するためのリアクティブなデータ
    const currentDate = ref('')
    
    /**
     * 現在の日付を取得して表示用にフォーマットする関数
     */
    const getCurrentDate = () => {
      const now = new Date()
      currentDate.value = now.toLocaleDateString('ja-JP', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
    
    // コンポーネントがマウントされた時に日付を設定
    onMounted(() => {
      getCurrentDate()
    })
    
    return {
      currentDate
    }
  }
}
</script>

<style scoped>
/* このアプリについてページのスタイル */

.about {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
}

.about h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 3rem;
  font-size: 2.5rem;
}

.about h2 {
  color: #3498db;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid #ecf0f1;
  padding-bottom: 0.5rem;
}

.app-info,
.tech-stack,
.features,
.version-info {
  margin-bottom: 3rem;
  background-color: #f8f9fa;
  padding: 2rem;
  border-radius: 8px;
}

.app-info p {
  font-size: 1.1rem;
  line-height: 1.7;
  color: #555;
}

.tech-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.tech-item {
  background-color: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.tech-item h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.3rem;
}

.tech-item ul {
  list-style-type: none;
  padding: 0;
}

.tech-item li {
  padding: 0.5rem 0;
  border-bottom: 1px solid #ecf0f1;
  color: #666;
}

.tech-item li:last-child {
  border-bottom: none;
}

.feature-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.feature-item {
  background-color: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.feature-item h3 {
  color: #e74c3c;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.feature-item p {
  color: #666;
  line-height: 1.6;
}

.version-card {
  background-color: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.version-card p {
  margin-bottom: 0.5rem;
  color: #555;
  font-size: 1.1rem;
}

.version-card p:last-child {
  margin-bottom: 0;
}
</style>
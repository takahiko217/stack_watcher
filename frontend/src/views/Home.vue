<!-- 
  ホームページコンポーネント
  
  アプリケーションのメインページです。
  初心者向けにコメントを豊富に含めています。
-->

<template>
  <div class="home">
    <!-- ページタイトル -->
    <h1>Stack Watcher へようこそ</h1>
    
    <!-- 説明文 -->
    <div class="welcome-section">
      <p>Stack Watcher は技術スタックを監視するためのアプリケーションです。</p>
      <p>Vue.js と FastAPI を使用して構築されています。</p>
    </div>
    
    <!-- 機能紹介セクション -->
    <div class="features-section">
      <h2>主な機能</h2>
      <div class="features-grid">
        <div class="feature-card">
          <h3>📊 リアルタイム監視</h3>
          <p>システムの状態をリアルタイムで監視できます</p>
        </div>
        <div class="feature-card">
          <h3>📈 データ可視化</h3>
          <p>わかりやすいグラフとチャートでデータを表示</p>
        </div>
        <div class="feature-card">
          <h3>🔔 アラート通知</h3>
          <p>問題が発生した際に即座に通知</p>
        </div>
        <div class="feature-card">
          <h3>📱 レスポンシブ対応</h3>
          <p>PC、タブレット、スマートフォンで利用可能</p>
        </div>
      </div>
    </div>
    
    <!-- APIステータス表示 -->
    <div class="api-status-section">
      <h2>API ステータス</h2>
      <div class="status-card" :class="{ 'connected': apiConnected, 'disconnected': !apiConnected }">
        <p v-if="apiConnected">✅ バックエンド API に接続されています</p>
        <p v-else>❌ バックエンド API に接続できません</p>
        <p class="status-message">{{ statusMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script>
/**
 * ホームページコンポーネント
 * 
 * アプリケーションのメインページの機能を提供します。
 */
import { ref, onMounted } from 'vue'

export default {
  name: 'Home',
  
  setup() {
    // リアクティブなデータを定義
    const apiConnected = ref(false)
    const statusMessage = ref('APIステータスを確認中...')
    
    /**
     * バックエンドAPIの接続状態を確認する関数
     */
    const checkApiStatus = async () => {
      try {
        // バックエンドAPIのヘルスチェックエンドポイントにリクエスト
        const response = await fetch('http://localhost:8000/health')
        
        if (response.ok) {
          const data = await response.json()
          apiConnected.value = true
          statusMessage.value = data.message || 'APIが正常に動作しています'
        } else {
          apiConnected.value = false
          statusMessage.value = 'APIからエラーレスポンスを受信しました'
        }
      } catch (error) {
        // エラーが発生した場合の処理
        apiConnected.value = false
        statusMessage.value = 'APIに接続できません。バックエンドサーバーが起動しているか確認してください。'
        console.error('API接続エラー:', error)
      }
    }
    
    // コンポーネントがマウントされた時にAPIステータスを確認
    onMounted(() => {
      checkApiStatus()
    })
    
    // テンプレートで使用するデータと関数を返す
    return {
      apiConnected,
      statusMessage
    }
  }
}
</script>

<style scoped>
/* 
  ホームページのスタイル
  
  scoped属性により、このコンポーネント内でのみ適用されます。
*/

.home {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.home h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 2rem;
  font-size: 2.5rem;
}

.welcome-section {
  background-color: #f8f9fa;
  padding: 2rem;
  border-radius: 8px;
  margin-bottom: 3rem;
  text-align: center;
}

.welcome-section p {
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 1rem;
  color: #555;
}

.features-section h2 {
  color: #2c3e50;
  margin-bottom: 2rem;
  text-align: center;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.feature-card {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-card h3 {
  color: #3498db;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.api-status-section h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
  text-align: center;
}

.status-card {
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  margin-bottom: 2rem;
}

.status-card.connected {
  background-color: #d4edda;
  border: 1px solid #c3e6cb;
  color: #155724;
}

.status-card.disconnected {
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  color: #721c24;
}

.status-message {
  margin-top: 1rem;
  font-style: italic;
}
</style>
<!-- 
  アプリケーションのルートコンポーネント
  
  このコンポーネントはアプリケーション全体のレイアウトを定義します。
  初心者向けにコメントを豊富に含めています。
-->

<template>
  <div id="app">
    <!-- ヘッダー部分 -->
    <header class="app-header">
      <h1>Stack Watcher</h1>
      <nav>
        <!-- ナビゲーションメニュー -->
        <router-link to="/">ホーム</router-link>
        <router-link to="/about">このアプリについて</router-link>
      </nav>
    </header>
    
    <!-- メインコンテンツ部分 -->
    <!-- router-viewは現在のルートに対応するコンポーネントを表示 -->
    <main class="app-main">
      <router-view />
    </main>
    
    <!-- フッター部分 -->
    <footer class="app-footer">
      <p>&copy; 2024 Stack Watcher. すべての権利は保護されています。</p>
    </footer>
  </div>
</template>

<script>
/**
 * アプリケーションのルートコンポーネント
 * 
 * このコンポーネントはアプリケーション全体の基本構造を提供します。
 */
export default {
  name: 'App',
  
  // コンポーネントがマウントされた時に実行される処理
  mounted() {
    console.log('Stack Watcher アプリケーションが起動しました')
  }
}
</script>

<style>
/* 
  アプリケーション全体のスタイル
  
  基本的なレイアウトとスタイルを定義しています。
*/

/* リセットスタイル */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* アプリケーション全体のコンテナ */
#app {
  font-family: 'Helvetica Neue', Arial, 'Hiragino Kaku Gothic ProN', 'Hiragino Sans', Meiryo, sans-serif;
  color: #333;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* ヘッダーのスタイル */
.app-header {
  background-color: #2c3e50;
  color: white;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.app-header h1 {
  font-size: 1.5rem;
}

.app-header nav a {
  color: white;
  text-decoration: none;
  margin-left: 1rem;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.app-header nav a:hover,
.app-header nav a.router-link-active {
  background-color: #34495e;
}

/* メインコンテンツのスタイル */
.app-main {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

/* フッターのスタイル */
.app-footer {
  background-color: #ecf0f1;
  padding: 1rem;
  text-align: center;
  color: #7f8c8d;
}
</style>
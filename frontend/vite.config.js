import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// Vite設定ファイル
// Vue.jsアプリケーションのビルド設定を定義
export default defineConfig({
  // Vue.jsプラグインを使用
  plugins: [vue()],
  
  // 開発サーバーの設定
  server: {
    port: 3000,
    host: true,
    // バックエンドAPIへのプロキシ設定
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false
      }
    }
  },
  
  // パスエイリアスの設定
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  
  // ビルド設定
  build: {
    outDir: 'dist',
    sourcemap: true
  }
})
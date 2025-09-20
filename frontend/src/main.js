/**
 * Vue.js アプリケーションのメインエントリーポイント
 * 
 * このファイルはVue.jsアプリケーションの起動ポイントです。
 * 初心者向けにコメントを豊富に含めています。
 */

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router.js'
import App from './App.vue'

// Pinia（状態管理）のインスタンスを作成
// アプリケーション全体でデータを共有するために使用
const pinia = createPinia()

// Vue.jsアプリケーションのインスタンスを作成
const app = createApp(App)

// プラグインを使用
app.use(pinia)  // 状態管理
app.use(router) // ルーティング

// アプリケーションをHTMLの#app要素にマウント
app.mount('#app')
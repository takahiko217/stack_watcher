/**
 * Stack Watcher - Vue.js メインエントリーポイント
 * 
 * 株価比較ツールのフロントエンドアプリケーション
 */

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router.js'
import './style.css'

// Vue.jsアプリケーションのインスタンスを作成
const app = createApp(App)

// Pinia（状態管理）を設定
const pinia = createPinia()
app.use(pinia)

// Vue Routerを設定
app.use(router)

// アプリケーションをHTMLの#root要素にマウント  
app.mount('#root')
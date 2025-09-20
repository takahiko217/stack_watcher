/**
 * Vue.js アプリケーションのメインエントリーポイント
 * 
 * このファイルはVue.jsアプリケーションの起動ポイントです。
 * シンプルなHello Worldアプリです。
 */

import { createApp } from 'vue'
import App from './App.vue'

// Vue.jsアプリケーションのインスタンスを作成
const app = createApp(App)

// アプリケーションをHTMLの#root要素にマウント  
app.mount('#root')
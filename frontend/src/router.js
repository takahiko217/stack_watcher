/**
 * Vue Router 設定ファイル
 * 
 * アプリケーションのルーティング（画面遷移）を管理します。
 * 初心者向けにコメントを豊富に含めています。
 */

import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import About from '../views/About.vue'

/**
 * ルートの定義
 * 
 * 各ルートは以下の要素を含みます：
 * - path: URLのパス
 * - name: ルートの名前
 * - component: 表示するコンポーネント
 */
const routes = [
  {
    path: '/',           // ホームページのURL
    name: 'Home',        // ルートの名前
    component: Home      // 表示するコンポーネント
  },
  {
    path: '/about',      // このアプリについてページのURL
    name: 'About',       // ルートの名前
    component: About     // 表示するコンポーネント
  }
]

/**
 * ルーターのインスタンスを作成
 * 
 * createWebHistory: HTML5のHistory APIを使用
 * これにより、URLが美しく表示されます（#なしのURL）
 */
const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
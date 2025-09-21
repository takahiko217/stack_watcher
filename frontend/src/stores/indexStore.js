/**
 * インデックスデータ管理Store
 * 日経225、TOPIX、マザーズ指数のデータを管理
 */

import { defineStore } from 'pinia'
import axios from 'axios'

export const useIndexStore = defineStore('index', {
  state: () => ({
    indices: [],           // インデックスデータ配列
    selectedPeriod: '7d',  // 選択中の期間
    isLoading: false,      // ローディング状態
    error: null,           // エラー情報
    lastUpdated: null      // 最終更新時刻
  }),

  getters: {
    hasData: (state) => state.indices.length > 0,
    
    // 銘柄別データ取得
    nikkeiData: (state) => state.indices.find(index => index.symbol === '^N225'),
    topixData: (state) => state.indices.find(index => index.symbol === '^TPX'),
    mothersData: (state) => state.indices.find(index => index.symbol === '2516.T'),
    
    // 全インデックスの日付配列（同期用）
    allDates: (state) => {
      if (state.indices.length > 0) {
        return state.indices[0].dates || []
      }
      return []
    },
    
    // ローディング状態
    isDataLoading: (state) => state.isLoading
  },

  actions: {
    async fetchIndices(period = null) {
      this.isLoading = true
      this.error = null
      
      const targetPeriod = period || this.selectedPeriod
      
      try {
        console.log('fetchIndices called, period:', targetPeriod)
        
        // 環境に応じてベースURLを設定
        const baseURL = window.location.hostname === 'localhost' 
          ? 'http://localhost:8003'
          : ''
        
        const url = `${baseURL}/api/v1/indices?period=${targetPeriod}`
        console.log('Index API request URL:', url)
        
        const response = await axios.get(url)
        console.log('Index API response:', response.data)
        
        if (response.data.success) {
          // データを配列形式に変換
          this.indices = Object.values(response.data.data)
          this.lastUpdated = response.data.lastUpdated
          console.log('Indices updated:', this.indices.length, 'indices loaded')
        } else {
          throw new Error('インデックスデータの取得に失敗しました')
        }
        
      } catch (error) {
        console.error('インデックスデータ取得エラー:', error)
        this.error = error.message
        this.indices = []
      } finally {
        this.isLoading = false
        console.log('fetchIndices completed, isLoading:', this.isLoading)
      }
    },

    setPeriod(period) {
      console.log('Index setPeriod called:', this.selectedPeriod, '->', period)
      this.selectedPeriod = period
      this.fetchIndices(period)
    },

    clearData() {
      this.indices = []
      this.error = null
      this.lastUpdated = null
    },

    // 特定のインデックスデータを取得
    async fetchSingleIndex(symbol, period = null) {
      const targetPeriod = period || this.selectedPeriod
      
      try {
        const baseURL = window.location.hostname === 'localhost' 
          ? 'http://localhost:8003'
          : ''
        
        const url = `${baseURL}/api/v1/indices/${symbol}?period=${targetPeriod}`
        const response = await axios.get(url)
        
        if (response.data.success) {
          // 既存データを更新または追加
          const existingIndex = this.indices.findIndex(index => index.symbol === symbol)
          if (existingIndex >= 0) {
            this.indices[existingIndex] = response.data.data
          } else {
            this.indices.push(response.data.data)
          }
        }
        
        return response.data
        
      } catch (error) {
        console.error(`インデックス ${symbol} の取得エラー:`, error)
        throw error
      }
    }
  }
})
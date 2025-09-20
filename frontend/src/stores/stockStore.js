/**
 * 株価データ管理用Store
 * バックエンドAPIとの通信とデータ管理を担当
 */

import { defineStore } from 'pinia'
import axios from 'axios'

// APIベースURL
const API_BASE_URL = 'http://localhost:8003/api/v1'

export const useStockStore = defineStore('stock', {
  // 状態（データ）
  state: () => ({
    // 株価データ
    stocks: [],
    
    // 選択された銘柄
    selectedSymbols: ['6326', '9984', '1377'],
    
    // 表示期間
    period: '7d',
    
    // 読み込み状態
    isLoading: false,
    
    // エラー情報
    error: null,
    
    // 最終更新日時
    lastUpdated: null,
    
    // 利用可能な銘柄一覧
    availableSymbols: []
  }),
  
  // 算出プロパティ（ゲッター）
  getters: {
    // 銘柄コードから株価データを取得
    getStockBySymbol: (state) => (symbol) => {
      return state.stocks.find(stock => stock.symbol === symbol)
    },
    
    // データが存在するかチェック
    hasData: (state) => state.stocks.length > 0,
    
    // チャート用にフォーマットされたデータ
    chartData: (state) => {
      return state.stocks.map(stock => ({
        name: stock.company_name,
        symbol: stock.symbol,
        data: stock.data_points.map(point => ({
          date: new Date(point.date).getTime(),
          value: point.close
        }))
      }))
    }
  },
  
  // アクション（メソッド）
  actions: {
    // 利用可能な銘柄一覧を取得
    async fetchAvailableSymbols() {
      try {
        const response = await axios.get(`${API_BASE_URL}/stocks/symbols`)
        
        if (response.data.success) {
          this.availableSymbols = response.data.data.symbols
        }
      } catch (error) {
        console.error('銘柄一覧取得エラー:', error)
        this.error = '銘柄一覧の取得に失敗しました'
      }
    },
    
    // 株価データを取得
    async fetchStocks() {
      console.log('fetchStocks called, period:', this.period, 'symbols:', this.selectedSymbols)
      this.isLoading = true
      this.error = null
      
      try {
        const symbols = this.selectedSymbols.join(',')
        const url = `${API_BASE_URL}/stocks?symbols=${symbols}&period=${this.period}`
        console.log('API request URL:', url)
        
        const response = await axios.get(url)
        console.log('API response:', response.data)
        
        if (response.data.success) {
          this.stocks = response.data.data.stocks
          this.lastUpdated = new Date()
          console.log('Stocks updated:', this.stocks.length, 'stocks loaded')
        } else {
          throw new Error(response.data.message || 'データ取得に失敗しました')
        }
      } catch (error) {
        console.error('株価データ取得エラー:', error)
        this.error = error.response?.data?.detail || error.message || 'データの取得に失敗しました'
        this.stocks = []
      } finally {
        this.isLoading = false
        console.log('fetchStocks completed, isLoading:', this.isLoading)
      }
    },
    
    // 表示期間を変更
    setPeriod(newPeriod) {
      console.log('setPeriod called:', this.period, '->', newPeriod)
      this.period = newPeriod
      this.fetchStocks()
    },
    
    // 銘柄を追加
    addSymbol(symbol) {
      if (!this.selectedSymbols.includes(symbol)) {
        this.selectedSymbols.push(symbol)
        this.fetchStocks()
      }
    },
    
    // 銘柄を削除
    removeSymbol(symbol) {
      this.selectedSymbols = this.selectedSymbols.filter(s => s !== symbol)
      this.stocks = this.stocks.filter(stock => stock.symbol !== symbol)
    },
    
    // エラーをクリア
    clearError() {
      this.error = null
    }
  }
})
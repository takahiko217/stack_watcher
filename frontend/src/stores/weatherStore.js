/**
 * 気象データ管理Store
 * 東京都の降水量、気温、気圧データを管理
 */

import { defineStore } from 'pinia'
import axios from 'axios'

export const useWeatherStore = defineStore('weather', {
  state: () => ({
    weatherData: null,     // 気象データオブジェクト
    selectedPeriod: '7d',  // 選択中の期間
    selectedLocation: 'tokyo', // 選択中の地域
    isLoading: false,      // ローディング状態
    error: null,           // エラー情報
    lastUpdated: null      // 最終更新時刻
  }),

  getters: {
    hasData: (state) => state.weatherData !== null,
    
    // 各気象要素のデータ
    precipitationData: (state) => state.weatherData?.precipitation || [],
    temperatureData: (state) => state.weatherData?.temperature || [],
    pressureData: (state) => state.weatherData?.pressure || [],
    
    // 日付配列（同期用）
    dates: (state) => state.weatherData?.dates || [],
    
    // 統計情報
    totalPrecipitation: (state) => {
      if (!state.weatherData?.precipitation) return 0
      return state.weatherData.precipitation.reduce((sum, val) => sum + val, 0)
    },
    
    averageTemperature: (state) => {
      if (!state.weatherData?.temperature) return 0
      const temps = state.weatherData.temperature
      return temps.reduce((sum, val) => sum + val, 0) / temps.length
    },
    
    averagePressure: (state) => {
      if (!state.weatherData?.pressure) return 0
      const pressures = state.weatherData.pressure
      return pressures.reduce((sum, val) => sum + val, 0) / pressures.length
    },
    
    isDataLoading: (state) => state.isLoading
  },

  actions: {
    async fetchWeatherData(location = null, period = null) {
      this.isLoading = true
      this.error = null
      
      const targetLocation = location || this.selectedLocation
      const targetPeriod = period || this.selectedPeriod
      
      try {
        console.log('fetchWeatherData called, location:', targetLocation, 'period:', targetPeriod)
        
        // 環境に応じてベースURLを設定
        const baseURL = window.location.hostname === 'localhost' 
          ? 'http://localhost:8003'
          : ''
        
        const url = `${baseURL}/api/v1/weather?location=${targetLocation}&period=${targetPeriod}`
        console.log('Weather API request URL:', url)
        
        const response = await axios.get(url)
        console.log('Weather API response:', response.data)
        
        if (response.data.success) {
          this.weatherData = response.data.data
          this.lastUpdated = response.data.lastUpdated
          console.log('Weather data updated:', this.weatherData.dates?.length, 'days loaded')
        } else {
          throw new Error('気象データの取得に失敗しました')
        }
        
      } catch (error) {
        console.error('気象データ取得エラー:', error)
        this.error = error.message
        this.weatherData = null
      } finally {
        this.isLoading = false
        console.log('fetchWeatherData completed, isLoading:', this.isLoading)
      }
    },

    setPeriod(period) {
      console.log('Weather setPeriod called:', this.selectedPeriod, '->', period)
      this.selectedPeriod = period
      this.fetchWeatherData(null, period)
    },

    setLocation(location) {
      console.log('Weather setLocation called:', this.selectedLocation, '->', location)
      this.selectedLocation = location
      this.fetchWeatherData(location, null)
    },

    clearData() {
      this.weatherData = null
      this.error = null
      this.lastUpdated = null
    },

    // 利用可能な観測地点を取得
    async fetchAvailableLocations() {
      try {
        const baseURL = window.location.hostname === 'localhost' 
          ? 'http://localhost:8003'
          : ''
        
        const url = `${baseURL}/api/v1/weather/locations`
        const response = await axios.get(url)
        
        return response.data
        
      } catch (error) {
        console.error('利用可能地点取得エラー:', error)
        throw error
      }
    }
  }
})
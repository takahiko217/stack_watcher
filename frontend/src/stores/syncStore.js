/**
 * グラフ同期状態管理Store
 * 複数グラフ間の横軸同期、ズーム、スライド操作を管理
 */

import { defineStore } from 'pinia'

export const useSyncStore = defineStore('sync', {
  state: () => ({
    // 選択中の期間（全グラフ共通）
    globalPeriod: '7d',
    
    // 同期設定
    syncSettings: {
      enableSync: true,        // 同期機能有効/無効
      syncZoom: true,          // ズーム同期
      syncPan: true,           // パン（スライド）同期
      syncSelection: true      // 選択範囲同期
    },
    
    // 現在の表示範囲
    currentRange: {
      startDate: null,
      endDate: null,
      zoomLevel: 1
    },
    
    // 各チャートの参照保持
    chartRefs: {
      stockChart: null,
      indexChart: null,
      weatherChart: null
    },
    
    // 同期イベントのフラグ（無限ループ防止）
    isSyncing: false,
    
    // 期間オプション
    periodOptions: [
      { value: '7d', label: '7日間', days: 7 },
      { value: '1m', label: '1ヶ月', days: 30 },
      { value: '3m', label: '四半期', days: 90 }
    ]
  }),

  getters: {
    // 現在の期間情報
    currentPeriodInfo: (state) => {
      return state.periodOptions.find(option => option.value === state.globalPeriod)
    },
    
    // 同期が有効かどうか
    isSyncEnabled: (state) => state.syncSettings.enableSync,
    
    // 登録されているチャート数
    registeredChartsCount: (state) => {
      return Object.values(state.chartRefs).filter(ref => ref !== null).length
    },
    
    // すべてのチャートが登録されているか
    allChartsRegistered: (state) => {
      return Object.values(state.chartRefs).every(ref => ref !== null)
    }
  },

  actions: {
    // 期間変更（全Store連携）
    setPeriod(period) {
      console.log('Sync setPeriod called:', this.globalPeriod, '->', period)
      
      if (!this.periodOptions.some(option => option.value === period)) {
        console.error('Invalid period:', period)
        return
      }
      
      this.globalPeriod = period
      
      // 他のStoreの期間も同期
      const stockStore = useStockStore()
      const indexStore = useIndexStore()
      const weatherStore = useWeatherStore()
      
      stockStore.setPeriod(period)
      indexStore.setPeriod(period)
      weatherStore.setPeriod(period)
    },
    
    // チャート参照を登録
    registerChart(chartType, chartInstance) {
      console.log('Registering chart:', chartType)
      
      if (chartType in this.chartRefs) {
        this.chartRefs[chartType] = chartInstance
        
        // チャートにイベントリスナーを設定
        this.setupChartEventListeners(chartType, chartInstance)
      } else {
        console.error('Unknown chart type:', chartType)
      }
    },
    
    // チャート参照を削除
    unregisterChart(chartType) {
      console.log('Unregistering chart:', chartType)
      
      if (chartType in this.chartRefs) {
        this.chartRefs[chartType] = null
      }
    },
    
    // チャートイベントリスナー設定
    setupChartEventListeners(chartType, chartInstance) {
      if (!this.syncSettings.enableSync) return
      
      // ズーム/パンイベントの監視
      chartInstance.on('dataZoom', (params) => {
        if (!this.isSyncing && this.syncSettings.syncZoom) {
          this.syncZoomToOtherCharts(chartType, params)
        }
      })
      
      // 選択範囲変更イベントの監視
      chartInstance.on('brush', (params) => {
        if (!this.isSyncing && this.syncSettings.syncSelection) {
          this.syncSelectionToOtherCharts(chartType, params)
        }
      })
    },
    
    // 他のチャートにズーム状態を同期
    syncZoomToOtherCharts(sourceChartType, zoomParams) {
      this.isSyncing = true
      
      try {
        Object.keys(this.chartRefs).forEach(chartType => {
          if (chartType !== sourceChartType && this.chartRefs[chartType]) {
            const chart = this.chartRefs[chartType]
            
            // ズーム状態を他のチャートに適用
            chart.dispatchAction({
              type: 'dataZoom',
              startValue: zoomParams.startValue,
              endValue: zoomParams.endValue
            })
          }
        })
        
        // 表示範囲を更新
        this.currentRange.startDate = zoomParams.startValue
        this.currentRange.endDate = zoomParams.endValue
        
      } finally {
        this.isSyncing = false
      }
    },
    
    // 他のチャートに選択範囲を同期
    syncSelectionToOtherCharts(sourceChartType, selectionParams) {
      this.isSyncing = true
      
      try {
        Object.keys(this.chartRefs).forEach(chartType => {
          if (chartType !== sourceChartType && this.chartRefs[chartType]) {
            const chart = this.chartRefs[chartType]
            
            // 選択範囲を他のチャートに適用
            chart.dispatchAction({
              type: 'brush',
              areas: selectionParams.areas
            })
          }
        })
        
      } finally {
        this.isSyncing = false
      }
    },
    
    // 同期設定変更
    updateSyncSettings(newSettings) {
      this.syncSettings = { ...this.syncSettings, ...newSettings }
      console.log('Sync settings updated:', this.syncSettings)
    },
    
    // 同期機能のオン/オフ切り替え
    toggleSync() {
      this.syncSettings.enableSync = !this.syncSettings.enableSync
      console.log('Sync toggled:', this.syncSettings.enableSync)
    },
    
    // 全チャートのズームリセット
    resetZoom() {
      if (!this.allChartsRegistered) return
      
      Object.values(this.chartRefs).forEach(chart => {
        if (chart) {
          chart.dispatchAction({
            type: 'dataZoom',
            start: 0,
            end: 100
          })
        }
      })
      
      this.currentRange.startDate = null
      this.currentRange.endDate = null
      this.currentRange.zoomLevel = 1
    },
    
    // 全チャートのリサイズ
    resizeAllCharts() {
      Object.values(this.chartRefs).forEach(chart => {
        if (chart) {
          chart.resize()
        }
      })
    }
  }
})

// 他のStoreとの循環参照を避けるため、必要時にインポート
import { useStockStore } from './stockStore'
import { useIndexStore } from './indexStore'
import { useWeatherStore } from './weatherStore'
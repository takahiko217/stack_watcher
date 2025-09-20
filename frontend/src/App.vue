<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <!-- ヘッダー -->
    <header class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center">
            <h1 class="text-2xl font-bold text-gray-900">Stock Watcher</h1>
            <span class="ml-3 text-sm text-gray-500">株価比較ツール</span>
          </div>
          
          <!-- 期間選択 -->
          <div class="flex items-center space-x-4">
            <div class="flex space-x-2">
              <button 
                v-for="periodOption in periodOptions" 
                :key="periodOption.value"
                @click="setPeriod(periodOption.value)"
                :class="[
                  'px-3 py-1 rounded-md text-sm font-medium transition-colors',
                  stockStore.period === periodOption.value 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                ]"
              >
                {{ periodOption.label }}
              </button>
            </div>
            
            <button 
              @click="refreshData"
              :disabled="stockStore.isLoading"
              class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="stockStore.isLoading" class="inline-block spinner mr-2"></span>
              {{ stockStore.isLoading ? '読み込み中...' : '更新' }}
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- メインコンテンツ -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- エラー表示 -->
      <div 
        v-if="stockStore.error" 
        class="mb-6 bg-red-50 border border-red-200 rounded-md p-4"
      >
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800">エラーが発生しました</h3>
            <div class="mt-2 text-sm text-red-700">
              {{ stockStore.error }}
            </div>
            <div class="mt-4">
              <button 
                @click="stockStore.clearError()" 
                class="text-sm bg-red-100 text-red-800 px-3 py-1 rounded-md hover:bg-red-200"
              >
                閉じる
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 株価チャート -->
      <div class="chart-container">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-medium text-gray-900">株価推移</h2>
          <div class="flex items-center space-x-4">
            <!-- 銘柄凡例 -->
            <div class="flex items-center space-x-3">
              <div 
                v-for="stock in stockStore.stocks" 
                :key="stock.symbol"
                class="flex items-center space-x-1"
              >
                <div 
                  class="w-3 h-3 rounded-full"
                  :style="{ backgroundColor: getStockColor(stock.symbol) }"
                ></div>
                <span class="text-sm text-gray-600">{{ stock.company_name }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- チャート本体 -->
        <div class="w-full h-96 flex items-center justify-center bg-white rounded-lg border border-gray-200">
          <div v-if="stockStore.isLoading" class="text-center">
            <div class="inline-block w-8 h-8 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mb-2"></div>
            <p class="text-gray-500">データを読み込み中...</p>
          </div>
          <div v-else-if="!stockStore.hasData" class="text-center text-gray-500">
            <p>データがありません</p>
            <button @click="refreshData" class="mt-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">データを取得</button>
          </div>
          <div v-else ref="chartContainer" class="w-full h-full"></div>
        </div>
      </div>

      <!-- 最終更新時間 -->
      <div v-if="stockStore.lastUpdated" class="mt-4 text-center text-sm text-gray-500">
        最終更新: {{ formatDateTime(stockStore.lastUpdated) }}
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import { useStockStore } from './stores/stockStore.js'
import * as echarts from 'echarts'

// ストア
const stockStore = useStockStore()

// 期間オプション
const periodOptions = [
  { value: '7d', label: '7日' },
  { value: '1m', label: '1ヶ月' },
  { value: '3m', label: '3ヶ月' }
]

// チャートの参照
const chartContainer = ref(null)
let chartInstance = null

// 銘柄ごとの色設定
const stockColors = {
  '6326': '#2563eb',  // クボタ - 青
  '9984': '#dc2626',  // ソフトバンク - 赤
  '1377': '#059669'   // サカタのタネ - 緑
}

// 銘柄の色を取得
const getStockColor = (symbol) => {
  return stockColors[symbol] || '#6b7280'
}

// 期間を設定
const setPeriod = (period) => {
  console.log('Period changed to:', period)
  stockStore.setPeriod(period)
}

// データを更新
const refreshData = () => {
  console.log('Refresh data clicked')
  stockStore.fetchStocks()
}

// 日時をフォーマット
const formatDateTime = (date) => {
  return new Date(date).toLocaleString('ja-JP')
}

// チャートを初期化
const initChart = async () => {
  if (!chartContainer.value) {
    console.log('Chart container not ready')
    return
  }
  
  // 既存のチャートインスタンスを破棄
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
  
  try {
    chartInstance = echarts.init(chartContainer.value)
    
    // 完全なチャートオプション（軸とシリーズを含む）
    const option = {
      title: {
        text: '',
        left: 'center'
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross'
        },
        formatter: function (params) {
          if (!params || params.length === 0) return ''
          
          let result = `<div style="font-size: 12px;">`
          result += `<div style="margin-bottom: 8px; font-weight: bold;">${new Date(params[0].data[0]).toLocaleDateString('ja-JP')}</div>`
          
          params.forEach(param => {
            result += `
              <div style="display: flex; align-items: center; margin-bottom: 4px;">
                <span style="display: inline-block; width: 8px; height: 8px; background-color: ${param.color}; border-radius: 50%; margin-right: 8px;"></span>
                <span style="margin-right: 16px;">${param.seriesName}</span>
                <span style="font-weight: bold;">¥${param.data[1].toLocaleString()}</span>
              </div>
            `
          })
          
          result += `</div>`
          return result
        }
      },
      legend: {
        show: false
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '10%',
        top: '10%',
        containLabel: true
      },
      xAxis: {
        type: 'time',
        boundaryGap: false,
        axisLine: {
          lineStyle: {
            color: '#e5e7eb'
          }
        },
        axisLabel: {
          color: '#6b7280',
          formatter: function (value) {
            return new Date(value).toLocaleDateString('ja-JP', { month: 'short', day: 'numeric' })
          }
        }
      },
      yAxis: {
        type: 'value',
        scale: true,
        axisLine: {
          show: false
        },
        axisTick: {
          show: false
        },
        axisLabel: {
          color: '#6b7280',
          formatter: function (value) {
            return '¥' + value.toLocaleString()
          }
        },
        splitLine: {
          lineStyle: {
            color: '#f3f4f6'
          }
        }
      },
      series: [] // 空のシリーズから開始
    }
    
    chartInstance.setOption(option)
    console.log('Chart initialized successfully')
  } catch (error) {
    console.error('Chart initialization error:', error)
  }
}

// チャートデータを更新
const updateChart = () => {
  if (!chartInstance || !stockStore.hasData) {
    console.log('Chart update skipped: no instance or no data')
    return
  }
  
  console.log('Updating chart with data:', stockStore.stocks.length, 'stocks')
  
  const series = stockStore.stocks.map(stock => ({
    name: stock.company_name,
    type: 'line',
    symbol: 'circle',
    symbolSize: 4,
    lineStyle: {
      width: 2,
      color: getStockColor(stock.symbol)
    },
    itemStyle: {
      color: getStockColor(stock.symbol)
    },
    data: stock.data_points.map(point => [
      new Date(point.date).getTime(),
      point.close
    ])
  }))
  
  // setTimeout を使ってメインプロセス外で実行
  setTimeout(() => {
    try {
      chartInstance.setOption({
        series: series
      }, false) // notMerge=false でマージ
      
      console.log('Chart updated successfully')
    } catch (error) {
      console.error('Chart update error:', error)
    }
  }, 0)
}

// データが変更されたらチャートを更新
watch(() => stockStore.stocks, (newStocks) => {
  console.log('Stocks data changed:', newStocks.length, 'stocks')
  if (stockStore.hasData && chartInstance) {
    // 次のTickで実行
    nextTick(() => {
      updateChart()
    })
  } else if (!stockStore.hasData && chartInstance) {
    // データがない場合はチャートをクリア
    setTimeout(() => {
      chartInstance.setOption({
        series: []
      }, false)
    }, 0)
  }
}, { deep: true })

// ローディング状態の監視
watch(() => stockStore.isLoading, (isLoading) => {
  console.log('Loading state changed:', isLoading)
  // ローディング完了時のみチャート更新
  if (!isLoading && stockStore.hasData && chartInstance) {
    nextTick(() => {
      updateChart()
    })
  }
})

// データ状態を監視してチャートを初期化（初回のみ）
watch(() => stockStore.hasData, (hasData) => {
  console.log('HasData changed:', hasData)
  if (hasData && chartContainer.value && !chartInstance) {
    nextTick(async () => {
      await initChart()
      updateChart()
    })
  }
})

// ウィンドウリサイズ対応
const handleResize = () => {
  if (chartInstance) {
    chartInstance.resize()
  }
}

// コンポーネントがマウントされた時
onMounted(async () => {
  console.log('=== Component mounted ===')
  console.log('chartContainer.value:', chartContainer.value)
  console.log('stockStore initial state:', {
    stocks: stockStore.stocks.length,
    selectedSymbols: stockStore.selectedSymbols,
    period: stockStore.period,
    isLoading: stockStore.isLoading,
    hasData: stockStore.hasData
  })
  
  // 初期データを取得
  console.log('Fetching initial data...')
  try {
    await stockStore.fetchStocks()
    console.log('Initial fetch completed, stocks:', stockStore.stocks.length)
  } catch (error) {
    console.error('Initial fetch error:', error)
  }
  
  // チャートコンテナが利用可能になるまで待つ
  await nextTick()
  console.log('After nextTick, chartContainer.value:', chartContainer.value)
  
  // データがある場合はチャートを初期化
  if (stockStore.hasData && chartContainer.value) {
    console.log('Initializing chart after mount...')
    try {
      await initChart()
      console.log('Chart initialization completed')
      updateChart()
      console.log('Initial chart update completed')
    } catch (error) {
      console.error('Chart initialization error:', error)
    }
  } else {
    console.log('Skipping chart init - hasData:', stockStore.hasData, 'chartContainer:', !!chartContainer.value)
  }
  
  // ウィンドウリサイズイベントを監視
  window.addEventListener('resize', handleResize)
  console.log('=== Mount process completed ===')
})

// コンポーネントがアンマウントされる前にクリーンアップ
import { onUnmounted } from 'vue'

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.dispose()
  }
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
/* Tailwind CSSを使用しているため、追加のスタイルは最小限 */

/* EChartsのカスタマイズ */
.chart-container {
  background: transparent;
}

/* スピナーアニメーション - Tailwindのanimate-spinを使用 */
</style>

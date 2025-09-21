<template>
  <div class="dashboard-container">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- ヘッダー -->
      <div class="dashboard-header">
        <h1 class="dashboard-title">Stack Watcher Dashboard</h1>
        <p class="dashboard-subtitle">株価・指数・気象データの統合監視</p>
      </div>

      <!-- 期間選択 -->
      <div class="period-selector-section">
        <PeriodSelector 
          :period="selectedPeriod"
          @update:period="updatePeriod"
        />
      </div>

      <!-- チャートセクション -->
      <div class="charts-grid">
        <!-- 株価チャート -->
        <div class="chart-card">
          <StockChart 
            :stock-data="stockData"
            :period="selectedPeriod"
            height="400px"
            @retry="fetchStockData"
          />
        </div>

        <!-- 指数チャート -->
        <div class="chart-card">
          <IndexChart 
            :index-data="indexData"
            :period="selectedPeriod"
            height="350px"
            @retry="fetchIndexData"
          />
        </div>

        <!-- 気象チャート -->
        <div class="chart-card">
          <WeatherChart 
            :weather-data="weatherData"
            :period="selectedPeriod"
            height="300px"
            @retry="fetchWeatherData"
          />
        </div>
      </div>

      <!-- API動作確認 -->
      <div class="api-test-section">
        <h2 class="api-title">API動作確認</h2>
        <div class="api-buttons">
          <button @click="testStockAPI" class="api-button">
            株価API テスト
          </button>
          <button @click="testIndexAPI" class="api-button">
            指数API テスト
          </button>
          <button @click="testWeatherAPI" class="api-button">
            気象API テスト
          </button>
        </div>
        
        <div v-if="apiResult" class="api-result">
          <h3 class="result-title">API レスポンス:</h3>
          <pre class="result-content">{{ apiResult }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import StockChart from '@/components/charts/StockChart.vue'
import WeatherChart from '@/components/charts/WeatherChart.vue'
import IndexChart from '@/components/charts/IndexChart.vue'
import PeriodSelector from '@/components/common/PeriodSelector.vue'

const apiResult = ref(null)
const stockData = ref({})
const indexData = ref({})
const weatherData = ref({})
const selectedPeriod = ref('7d')

// 株価データ取得
const fetchStockData = async () => {
  try {
    const response = await fetch(`/api/v1/stocks?symbols=6326,9984,1377&period=${selectedPeriod.value}`)
    const data = await response.json()
    stockData.value = data
  } catch (error) {
    console.error('株価データ取得エラー:', error)
  }
}

// 指数データ取得
const fetchIndexData = async () => {
  try {
    const response = await fetch(`/api/v1/indices?period=${selectedPeriod.value}`)
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }
    
    const data = await response.json()
    console.log('指数データ取得成功:', data)
    
    // APIレスポンスの形式を確認
    if (data.success && data.data) {
      indexData.value = data.data
    } else {
      indexData.value = data
    }
  } catch (error) {
    console.error('指数データ取得エラー:', error)
    indexData.value = {}
  }
}

// 期間変更時の処理
const updatePeriod = (newPeriod) => {
  selectedPeriod.value = newPeriod
  fetchStockData()
  fetchIndexData()
  fetchWeatherData()
}

// 気象データ取得
const fetchWeatherData = async () => {
  try {
    const response = await fetch(`/api/v1/weather?period=${selectedPeriod.value}`)
    const data = await response.json()
    weatherData.value = data
  } catch (error) {
    console.error('気象データ取得エラー:', error)
  }
}

const testStockAPI = async () => {
  try {
    const response = await fetch('/api/v1/stocks?symbols=6326,9984,1377')
    const data = await response.json()
    apiResult.value = JSON.stringify(data, null, 2)
  } catch (error) {
    apiResult.value = `エラー: ${error.message}`
  }
}

const testIndexAPI = async () => {
  try {
    const response = await fetch('/api/v1/indices?period=7d')
    const data = await response.json()
    apiResult.value = JSON.stringify(data, null, 2)
  } catch (error) {
    apiResult.value = `エラー: ${error.message}`
  }
}

const testWeatherAPI = async () => {
  try {
    const response = await fetch('/api/v1/weather?period=7d')
    const data = await response.json()
    apiResult.value = JSON.stringify(data, null, 2)
  } catch (error) {
    apiResult.value = `エラー: ${error.message}`
  }
}

// 初期化
onMounted(() => {
  fetchStockData()
  fetchIndexData()
  fetchWeatherData()
})
</script>

<style scoped>
.dashboard-container {
  @apply min-h-screen bg-gray-50;
}

.dashboard-header {
  @apply text-center mb-8;
}

.dashboard-title {
  @apply text-3xl font-bold text-gray-900 mb-2;
}

.dashboard-subtitle {
  @apply text-lg text-gray-600;
}

.period-selector-section {
  @apply bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6;
}

.charts-grid {
  @apply grid grid-cols-1 gap-6 mb-8;
}

.chart-card {
  @apply bg-white rounded-lg shadow-sm border border-gray-200;
}

.chart-card:has(.chart-placeholder) {
  @apply p-6;
}

.chart-title {
  @apply text-xl font-semibold text-gray-800 mb-4;
}

.chart-placeholder {
  @apply h-64 bg-gray-50 rounded-lg flex flex-col items-center justify-center;
}

.api-test-section {
  @apply bg-white rounded-lg shadow-sm border border-gray-200 p-6;
}

.api-title {
  @apply text-xl font-semibold text-gray-800 mb-4;
}

.api-buttons {
  @apply flex gap-4 mb-6;
}

.api-button {
  @apply px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors;
}

.api-result {
  @apply mt-4;
}

.result-title {
  @apply text-lg font-medium text-gray-700 mb-2;
}

.result-content {
  @apply bg-gray-100 p-4 rounded-md text-sm font-mono overflow-auto max-h-96;
}
</style>

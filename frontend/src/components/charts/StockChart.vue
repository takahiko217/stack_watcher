<template>
  <div class="stock-chart-container">
    <div class="chart-header">
      <h3 class="chart-title">株価データ</h3>
      <div class="chart-info">
        <span class="data-source">データソース: Yahoo Finance API</span>
        <span class="period">期間: {{ period }}</span>
      </div>
    </div>
    
    <div class="chart-content">
      <div ref="chartContainer" class="chart-main"></div>
      
      <div class="chart-legend">
        <div class="legend-item">
          <span class="legend-color kubota"></span>
          <span>クボタ (6326)</span>
        </div>
        <div class="legend-item">
          <span class="legend-color softbank"></span>
          <span>ソフトバンクグループ (9984)</span>
        </div>
        <div class="legend-item">
          <span class="legend-color sakata"></span>
          <span>サカタのタネ (1377)</span>
        </div>
      </div>
    </div>
    
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <span>株価データを読み込み中...</span>
    </div>
    
    <div v-if="error" class="error-message">
      <span>{{ error }}</span>
      <button @click="retryLoad" class="retry-button">再試行</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import * as echarts from 'echarts'

// Props
const props = defineProps({
  stockData: {
    type: Object,
    default: () => ({})
  },
  period: {
    type: String,
    default: '7d'
  },
  height: {
    type: String,
    default: '400px'
  }
})

// Emit
const emit = defineEmits(['retry'])

// Reactive data
const chartContainer = ref(null)
const chart = ref(null)
const loading = ref(false)
const error = ref('')

// Chart colors
const colors = {
  kubota: '#2563eb',    // 青
  softbank: '#dc2626',  // 赤
  sakata: '#059669'     // 緑
}

// Chart initialization
const initChart = () => {
  if (!chartContainer.value) return
  
  chart.value = echarts.init(chartContainer.value)
  updateChart()
  
  // Window resize handler
  window.addEventListener('resize', handleResize)
}

// Chart update
const updateChart = () => {
  if (!chart.value || !props.stockData?.data?.stocks) return
  
  const stocks = props.stockData.data.stocks
  
  // データの準備
  const series = stocks.map((stock, index) => {
    const colorKey = stock.symbol === '6326' ? 'kubota' : 
                     stock.symbol === '9984' ? 'softbank' : 'sakata'
    
    const data = stock.data_points.map(point => [
      point.date,
      point.close
    ])
    
    return {
      name: `${stock.company_name} (${stock.symbol})`,
      type: 'line',
      data: data,
      itemStyle: {
        color: colors[colorKey]
      },
      lineStyle: {
        color: colors[colorKey],
        width: 2
      },
      symbol: 'circle',
      symbolSize: 4,
      smooth: true
    }
  })
  
  const option = {
    title: {
      text: '',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      formatter: function(params) {
        const date = new Date(params[0].axisValue)
        let tooltip = `<div style="margin-bottom: 4px;">${date.getMonth() + 1}/${date.getDate()}</div>`
        
        params.forEach(param => {
          tooltip += `<div style="display: flex; align-items: center; margin-bottom: 2px;">
            <span style="display: inline-block; width: 10px; height: 10px; background-color: ${param.color}; border-radius: 50%; margin-right: 8px;"></span>
            ${param.seriesName}: ¥${param.value[1].toLocaleString()}
          </div>`
        })
        
        return tooltip
      }
    },
    legend: {
      show: false // カスタム凡例を使用
    },
    grid: {
      left: '60px',
      right: '60px',
      bottom: '60px',
      top: '40px',
      containLabel: false
    },
    xAxis: {
      type: 'time',
      axisLabel: {
        formatter: function(value) {
          const date = new Date(value)
          return `${date.getMonth() + 1}/${date.getDate()}`
        }
      }
    },
    yAxis: {
      type: 'value',
      name: '株価 (円)',
      axisLabel: {
        formatter: function(value) {
          return `¥${value.toLocaleString()}`
        }
      },
      splitLine: {
        show: true,
        lineStyle: {
          color: '#e5e7eb',
          type: 'dashed'
        }
      }
    },
    series: series,
    animation: true,
    animationDuration: 800
  }
  
  chart.value.setOption(option, true)
}

// Window resize handler
const handleResize = () => {
  if (chart.value) {
    chart.value.resize()
  }
}

// Retry load
const retryLoad = () => {
  error.value = ''
  emit('retry')
}

// Watchers
watch(() => props.stockData, () => {
  updateChart()
}, { deep: true })

watch(() => props.period, () => {
  updateChart()
})

// Lifecycle
onMounted(async () => {
  await nextTick()
  initChart()
})

onUnmounted(() => {
  if (chart.value) {
    chart.value.dispose()
    chart.value = null
  }
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.stock-chart-container {
  @apply relative bg-white rounded-lg shadow-sm border border-gray-200;
  min-height: 400px;
}

.chart-header {
  @apply flex justify-between items-center p-4 border-b border-gray-100;
}

.chart-title {
  @apply text-lg font-semibold text-gray-800;
}

.chart-info {
  @apply text-sm text-gray-500 space-x-4;
}

.chart-content {
  @apply relative;
}

.chart-main {
  height: v-bind(height);
  @apply w-full;
}

.chart-legend {
  @apply flex justify-center space-x-6 py-3 bg-gray-50 border-t border-gray-100;
}

.legend-item {
  @apply flex items-center space-x-2 text-sm text-gray-600;
}

.legend-color {
  @apply w-3 h-3 rounded-full;
}

.legend-color.kubota {
  background-color: v-bind('colors.kubota');
}

.legend-color.softbank {
  background-color: v-bind('colors.softbank');
}

.legend-color.sakata {
  background-color: v-bind('colors.sakata');
}

.loading-overlay {
  @apply absolute inset-0 bg-white bg-opacity-75 flex flex-col items-center justify-center;
}

.loading-spinner {
  @apply w-8 h-8 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mb-2;
}

.error-message {
  @apply absolute inset-0 bg-red-50 flex flex-col items-center justify-center text-red-600;
}

.retry-button {
  @apply mt-2 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition-colors;
}
</style>
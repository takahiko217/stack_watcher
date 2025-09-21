<template>
  <div class="weather-chart-container">
    <div class="chart-header">
      <h3 class="chart-title">気象データ</h3>
      <div class="chart-info">
        <span class="data-source">データソース: OpenMeteo API</span>
        <span class="location">東京都</span>
      </div>
    </div>
    
    <div class="chart-content">
      <div ref="chartContainer" class="chart-main"></div>
      
      <div class="chart-legend">
        <div class="legend-item">
          <span class="legend-color precipitation"></span>
          <span>降水量 (mm)</span>
        </div>
        <div class="legend-item">
          <span class="legend-color temperature"></span>
          <span>気温 (℃)</span>
        </div>
        <div class="legend-item">
          <span class="legend-color pressure"></span>
          <span>気圧 (hPa)</span>
        </div>
      </div>
    </div>
    
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <span>気象データを読み込み中...</span>
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
  weatherData: {
    type: Object,
    default: () => ({})
  },
  period: {
    type: String,
    default: '7d'
  },
  height: {
    type: String,
    default: '300px'
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
  precipitation: '#0ea5e9', // スカイブルー
  temperature: '#ef4444',   // レッド
  pressure: '#6b7280'       // グレー
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
  if (!chart.value || !props.weatherData?.data) return
  
  const data = props.weatherData.data
  
  const option = {
    title: {
      text: '',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      formatter: function(params) {
        let tooltip = `<div style="margin-bottom: 4px;">${params[0].axisValue}</div>`
        
        params.forEach(param => {
          const unit = param.seriesName === '降水量' ? 'mm' : 
                      param.seriesName === '気温' ? '℃' : 'hPa'
          tooltip += `<div style="display: flex; align-items: center; margin-bottom: 2px;">
            <span style="display: inline-block; width: 10px; height: 10px; background-color: ${param.color}; border-radius: 50%; margin-right: 8px;"></span>
            ${param.seriesName}: ${param.value}${unit}
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
      type: 'category',
      data: data.dates || [],
      axisLabel: {
        formatter: function(value) {
          const date = new Date(value)
          return `${date.getMonth() + 1}/${date.getDate()}`
        }
      }
    },
    yAxis: [
      {
        type: 'value',
        name: '降水量(mm) / 気温(℃)',
        position: 'left',
        axisLabel: {
          formatter: '{value}'
        },
        splitLine: {
          show: true,
          lineStyle: {
            color: '#e5e7eb',
            type: 'dashed'
          }
        }
      },
      {
        type: 'value',
        name: '気圧(hPa)',
        position: 'right',
        axisLabel: {
          formatter: '{value}'
        },
        splitLine: {
          show: false
        }
      }
    ],
    series: [
      {
        name: '降水量',
        type: 'bar',
        yAxisIndex: 0,
        data: data.precipitation || [],
        itemStyle: {
          color: colors.precipitation
        },
        barWidth: '40%'
      },
      {
        name: '気温',
        type: 'line',
        yAxisIndex: 0,
        data: data.temperature || [],
        itemStyle: {
          color: colors.temperature
        },
        lineStyle: {
          color: colors.temperature,
          width: 2
        },
        symbol: 'circle',
        symbolSize: 4,
        smooth: true
      },
      {
        name: '気圧',
        type: 'line',
        yAxisIndex: 1,
        data: data.pressure || [],
        itemStyle: {
          color: colors.pressure
        },
        lineStyle: {
          color: colors.pressure,
          width: 2,
          type: 'dashed'
        },
        symbol: 'diamond',
        symbolSize: 4,
        smooth: true
      }
    ],
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
watch(() => props.weatherData, () => {
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
.weather-chart-container {
  @apply relative bg-white rounded-lg shadow-sm border border-gray-200;
  min-height: 300px;
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

.legend-color.precipitation {
  background-color: v-bind('colors.precipitation');
}

.legend-color.temperature {
  background-color: v-bind('colors.temperature');
}

.legend-color.pressure {
  background-color: v-bind('colors.pressure');
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
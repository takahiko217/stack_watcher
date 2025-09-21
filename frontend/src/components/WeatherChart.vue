<template>
  <div class="weather-chart-container">
    <!-- ヘッダー -->
    <div class="chart-header">
      <h3 class="chart-title">気象データ（東京都）</h3>
      <div class="chart-info">
        <span v-if="isLoading" class="loading-text">データ読み込み中...</span>
        <span v-else-if="hasData" class="data-count">{{ dates.length }}日分</span>
        <span v-else class="no-data">データなし</span>
      </div>
    </div>

    <!-- 統計サマリー -->
    <div v-if="hasData" class="stats-summary">
      <div class="stat-item">
        <span class="stat-label">総降水量</span>
        <span class="stat-value text-blue-600">{{ totalPrecipitation.toFixed(1) }}mm</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">平均気温</span>
        <span class="stat-value text-red-500">{{ averageTemperature.toFixed(1) }}°C</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">平均気圧</span>
        <span class="stat-value text-gray-600">{{ averagePressure.toFixed(1) }}hPa</span>
      </div>
    </div>

    <!-- チャート本体 -->
    <div 
      ref="chartContainer" 
      class="chart-content"
      :class="{ 'loading': isLoading }"
    ></div>

    <!-- エラー表示 -->
    <div v-if="error" class="error-message">
      <svg class="error-icon" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
      </svg>
      {{ error }}
    </div>

    <!-- 凡例 -->
    <div v-if="hasData" class="legend">
      <div class="legend-item">
        <div class="legend-color" style="background-color: #0ea5e9;"></div>
        <span class="legend-name">降水量 (mm)</span>
      </div>
      <div class="legend-item">
        <div class="legend-color" style="background-color: #ef4444;"></div>
        <span class="legend-name">気温 (°C)</span>
      </div>
      <div class="legend-item">
        <div class="legend-color" style="background-color: #6b7280;"></div>
        <span class="legend-name">気圧 (hPa)</span>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, watch, computed, nextTick } from 'vue'
import * as echarts from 'echarts'
import { useWeatherStore } from '../stores/weatherStore'
import { useSyncStore } from '../stores/syncStore'

export default {
  name: 'WeatherChart',
  props: {
    height: {
      type: String,
      default: '300px'
    }
  },
  setup(props) {
    const chartContainer = ref(null)
    const chartInstance = ref(null)
    
    const weatherStore = useWeatherStore()
    const syncStore = useSyncStore()

    // ストアからのデータ
    const weatherData = computed(() => weatherStore.weatherData)
    const isLoading = computed(() => weatherStore.isLoading)
    const error = computed(() => weatherStore.error)
    const hasData = computed(() => weatherStore.hasData)

    // 各データ系列
    const dates = computed(() => weatherStore.dates)
    const precipitationData = computed(() => weatherStore.precipitationData)
    const temperatureData = computed(() => weatherStore.temperatureData)
    const pressureData = computed(() => weatherStore.pressureData)

    // 統計値
    const totalPrecipitation = computed(() => weatherStore.totalPrecipitation)
    const averageTemperature = computed(() => weatherStore.averageTemperature)
    const averagePressure = computed(() => weatherStore.averagePressure)

    // チャート初期化
    const initChart = () => {
      if (!chartContainer.value || !hasData.value) return

      // 既存チャートを破棄
      if (chartInstance.value) {
        chartInstance.value.dispose()
      }

      // 新しいチャートインスタンス作成
      chartInstance.value = echarts.init(chartContainer.value)
      
      // 同期ストアに登録
      syncStore.registerChart('weatherChart', chartInstance.value)

      updateChart()
    }

    // チャート更新
    const updateChart = () => {
      if (!chartInstance.value || !hasData.value) return

      const option = {
        title: {
          show: false
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            label: {
              backgroundColor: '#6a7985'
            }
          },
          formatter: function(params) {
            let tooltipText = `<div class="font-medium">${params[0].axisValue}</div>`
            
            params.forEach(param => {
              let unit = ''
              let color = param.color
              
              switch(param.seriesName) {
                case '降水量':
                  unit = 'mm'
                  break
                case '気温':
                  unit = '°C'
                  break
                case '気圧':
                  unit = 'hPa'
                  break
              }
              
              tooltipText += `
                <div class="flex justify-between items-center mt-1">
                  <span style="color: ${color}">${param.seriesName}:</span>
                  <span class="font-mono">${param.value}${unit}</span>
                </div>
              `
            })
            
            return tooltipText
          }
        },
        legend: {
          show: false  // カスタム凡例を使用
        },
        grid: {
          left: '3%',
          right: '8%',
          bottom: '10%',
          top: '10%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: dates.value,
          axisLine: {
            lineStyle: {
              color: '#e5e7eb'
            }
          },
          axisLabel: {
            color: '#6b7280',
            fontSize: 12
          }
        },
        yAxis: [
          {
            // 左Y軸: 降水量
            type: 'value',
            name: '降水量 (mm)',
            position: 'left',
            axisLine: {
              lineStyle: {
                color: '#0ea5e9'
              }
            },
            axisLabel: {
              color: '#0ea5e9',
              fontSize: 12
            },
            splitLine: {
              show: false
            }
          },
          {
            // 右Y軸: 気温と気圧
            type: 'value',
            name: '気温 (°C) / 気圧 (hPa)',
            position: 'right',
            axisLine: {
              lineStyle: {
                color: '#6b7280'
              }
            },
            axisLabel: {
              color: '#6b7280',
              fontSize: 12
            },
            splitLine: {
              lineStyle: {
                color: '#f3f4f6',
                type: 'dashed'
              }
            }
          }
        ],
        series: [
          {
            name: '降水量',
            type: 'bar',
            yAxisIndex: 0,
            data: precipitationData.value,
            itemStyle: {
              color: '#0ea5e9'
            },
            barWidth: '60%'
          },
          {
            name: '気温',
            type: 'line',
            yAxisIndex: 1,
            data: temperatureData.value,
            smooth: true,
            symbol: 'circle',
            symbolSize: 4,
            lineStyle: {
              width: 2,
              color: '#ef4444'
            },
            itemStyle: {
              color: '#ef4444'
            }
          },
          {
            name: '気圧',
            type: 'line',
            yAxisIndex: 1,
            data: pressureData.value,
            smooth: true,
            symbol: 'diamond',
            symbolSize: 4,
            lineStyle: {
              width: 2,
              color: '#6b7280',
              type: 'dashed'
            },
            itemStyle: {
              color: '#6b7280'
            }
          }
        ],
        dataZoom: [
          {
            type: 'inside',
            start: 0,
            end: 100
          }
        ],
        animation: true,
        animationDuration: 1000
      }

      chartInstance.value.setOption(option, true)
    }

    // チャートリサイズ
    const handleResize = () => {
      if (chartInstance.value) {
        chartInstance.value.resize()
      }
    }

    // ライフサイクル
    onMounted(async () => {
      // 初期データ取得
      if (!hasData.value) {
        await weatherStore.fetchWeatherData()
      }
      
      await nextTick()
      initChart()
      
      // リサイズイベント監視
      window.addEventListener('resize', handleResize)
    })

    onUnmounted(() => {
      if (chartInstance.value) {
        syncStore.unregisterChart('weatherChart')
        chartInstance.value.dispose()
      }
      window.removeEventListener('resize', handleResize)
    })

    // データ変更監視
    watch(hasData, async (newValue) => {
      if (newValue) {
        await nextTick()
        initChart()
      }
    })

    watch(weatherData, () => {
      if (chartInstance.value && hasData.value) {
        updateChart()
      }
    }, { deep: true })

    return {
      chartContainer,
      weatherData,
      isLoading,
      error,
      hasData,
      dates,
      precipitationData,
      temperatureData,
      pressureData,
      totalPrecipitation,
      averageTemperature,
      averagePressure
    }
  }
}
</script>

<style scoped>
.weather-chart-container {
  @apply bg-white rounded-lg shadow-sm border border-gray-200 p-4;
}

.chart-header {
  @apply flex justify-between items-center mb-4;
}

.chart-title {
  @apply text-lg font-semibold text-gray-800;
}

.chart-info {
  @apply text-sm text-gray-500;
}

.loading-text {
  @apply text-blue-600;
}

.data-count {
  @apply text-green-600;
}

.no-data {
  @apply text-gray-400;
}

.stats-summary {
  @apply grid grid-cols-3 gap-4 mb-4 p-3 bg-gray-50 rounded-md;
}

.stat-item {
  @apply text-center;
}

.stat-label {
  @apply block text-xs text-gray-500 mb-1;
}

.stat-value {
  @apply block text-sm font-semibold;
}

.chart-content {
  height: v-bind(height);
  @apply w-full;
}

.chart-content.loading {
  @apply flex items-center justify-center bg-gray-50 rounded;
}

.error-message {
  @apply flex items-center text-red-600 text-sm mt-2;
}

.error-icon {
  @apply w-4 h-4 mr-2;
}

.legend {
  @apply flex flex-wrap gap-4 mt-4 pt-4 border-t border-gray-100;
}

.legend-item {
  @apply flex items-center space-x-2;
}

.legend-color {
  @apply w-3 h-3 rounded-full;
}

.legend-name {
  @apply text-sm font-medium text-gray-700;
}

/* レスポンシブ対応 */
@media (max-width: 640px) {
  .chart-header {
    @apply flex-col items-start space-y-2;
  }
  
  .stats-summary {
    @apply grid-cols-1 gap-2;
  }
  
  .legend {
    @apply flex-col space-y-2;
  }
}
</style>
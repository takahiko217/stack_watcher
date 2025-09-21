<template>
  <div class="index-chart-container">
    <!-- ヘッダー -->
    <div class="chart-header">
      <h3 class="chart-title">株価指数</h3>
      <div class="chart-info">
        <span v-if="isLoading" class="loading-text">データ読み込み中...</span>
        <span v-else-if="hasData" class="data-count">{{ indices.length }}指数</span>
        <span v-else class="no-data">データなし</span>
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
      <div
        v-for="index in indices"
        :key="index.symbol"
        class="legend-item"
      >
        <div 
          class="legend-color"
          :style="{ backgroundColor: getIndexColor(index.symbol) }"
        ></div>
        <span class="legend-name">{{ index.name }}</span>
        <span 
          class="legend-value"
          :class="getChangeClass(index.changes[index.changes.length - 1])"
        >
          {{ formatValue(index.values[index.values.length - 1]) }}
          ({{ formatChange(index.changes[index.changes.length - 1]) }})
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, watch, computed, nextTick } from 'vue'
import * as echarts from 'echarts'
import { useIndexStore } from '../stores/indexStore'
import { useSyncStore } from '../stores/syncStore'

export default {
  name: 'IndexChart',
  props: {
    height: {
      type: String,
      default: '350px'
    }
  },
  setup(props) {
    const chartContainer = ref(null)
    const chartInstance = ref(null)
    
    const indexStore = useIndexStore()
    const syncStore = useSyncStore()

    // ストアからのデータ
    const indices = computed(() => indexStore.indices)
    const isLoading = computed(() => indexStore.isLoading)
    const error = computed(() => indexStore.error)
    const hasData = computed(() => indexStore.hasData)

    // インデックス色定義
    const indexColors = {
      '^N225': '#7c3aed',    // 紫（日経225）
      '^TPX': '#ea580c',     // オレンジ（TOPIX）
      '2516.T': '#f59e0b'    // アンバー（マザーズ指数）
    }

    // 色取得
    const getIndexColor = (symbol) => {
      return indexColors[symbol] || '#6b7280'
    }

    // 変化量に応じたクラス
    const getChangeClass = (change) => {
      if (change > 0) return 'text-green-600'
      if (change < 0) return 'text-red-600'
      return 'text-gray-600'
    }

    // 値フォーマット
    const formatValue = (value) => {
      if (typeof value !== 'number') return '-'
      return new Intl.NumberFormat('ja-JP', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      }).format(value)
    }

    // 変化量フォーマット
    const formatChange = (change) => {
      if (typeof change !== 'number') return ''
      const sign = change >= 0 ? '+' : ''
      return `${sign}${change.toFixed(2)}`
    }

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
      syncStore.registerChart('indexChart', chartInstance.value)

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
              const index = indices.value.find(idx => idx.name === param.seriesName)
              if (index) {
                const change = index.changes[param.dataIndex]
                const changePercent = index.changePercent[param.dataIndex]
                const changeClass = change >= 0 ? 'text-green-600' : 'text-red-600'
                
                tooltipText += `
                  <div class="flex justify-between items-center mt-1">
                    <span style="color: ${param.color}">${param.seriesName}:</span>
                    <div class="text-right">
                      <div>${formatValue(param.value)}</div>
                      <div class="${changeClass}">
                        ${formatChange(change)} (${changePercent.toFixed(2)}%)
                      </div>
                    </div>
                  </div>
                `
              }
            })
            
            return tooltipText
          }
        },
        legend: {
          show: false  // カスタム凡例を使用
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '10%',
          top: '10%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: indices.value[0]?.dates || [],
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
        yAxis: {
          type: 'value',
          scale: true,
          axisLine: {
            lineStyle: {
              color: '#e5e7eb'
            }
          },
          axisLabel: {
            color: '#6b7280',
            fontSize: 12,
            formatter: function(value) {
              return formatValue(value)
            }
          },
          splitLine: {
            lineStyle: {
              color: '#f3f4f6',
              type: 'dashed'
            }
          }
        },
        series: indices.value.map(index => ({
          name: index.name,
          type: 'line',
          data: index.values,
          smooth: true,
          symbol: 'circle',
          symbolSize: 4,
          lineStyle: {
            width: 2,
            color: getIndexColor(index.symbol)
          },
          itemStyle: {
            color: getIndexColor(index.symbol)
          },
          areaStyle: {
            opacity: 0.1,
            color: getIndexColor(index.symbol)
          }
        })),
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
        await indexStore.fetchIndices()
      }
      
      await nextTick()
      initChart()
      
      // リサイズイベント監視
      window.addEventListener('resize', handleResize)
    })

    onUnmounted(() => {
      if (chartInstance.value) {
        syncStore.unregisterChart('indexChart')
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

    watch(indices, () => {
      if (chartInstance.value && hasData.value) {
        updateChart()
      }
    }, { deep: true })

    return {
      chartContainer,
      indices,
      isLoading,
      error,
      hasData,
      getIndexColor,
      getChangeClass,
      formatValue,
      formatChange
    }
  }
}
</script>

<style scoped>
.index-chart-container {
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

.legend-value {
  @apply text-sm font-mono;
}

/* レスポンシブ対応 */
@media (max-width: 640px) {
  .chart-header {
    @apply flex-col items-start space-y-2;
  }
  
  .legend {
    @apply flex-col space-y-2;
  }
  
  .legend-item {
    @apply justify-between;
  }
}
</style>
<template>
  <div class="index-chart-container">
    <div ref="chartRef" class="chart-container"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  indexData: {
    type: Object,
    default: () => ({})
  },
  period: {
    type: String,
    default: '7d'
  }
})

const chartRef = ref(null)
let chartInstance = null

const initChart = () => {
  if (!chartRef.value) return
  
  chartInstance = echarts.init(chartRef.value)
  updateChart()
}

const updateChart = () => {
  if (!chartInstance) {
    console.warn('IndexChart: チャートインスタンスが初期化されていません')
    return
  }
  
  if (!props.indexData) {
    console.warn('IndexChart: indexData プロパティが未設定です')
    return
  }

  // APIレスポンスの構造に対応
  let indicesData = []
  let validIndices = []
  
  try {
    if (props.indexData.data) {
      // APIレスポンス形式: { success: true, data: { "^N225": {...}, "^TPX": {...} } }
      indicesData = Object.values(props.indexData.data)
    } else if (typeof props.indexData === 'object' && !Array.isArray(props.indexData)) {
      // 直接オブジェクト形式: { "^N225": {...}, "^TPX": {...} }
      indicesData = Object.values(props.indexData)
    } else {
      // 配列形式または不正な形式
      indicesData = Array.isArray(props.indexData) ? props.indexData : []
    }

    if (indicesData.length === 0) {
      console.warn('IndexChart: 指数データが空です', props.indexData)
      return
    }

    // データの検証
    validIndices = indicesData.filter(index => {
      const isValid = index && 
        index.dates && 
        index.values && 
        Array.isArray(index.dates) && 
        Array.isArray(index.values) &&
        index.dates.length > 0 &&
        index.values.length > 0
      
      if (!isValid) {
        console.warn('IndexChart: 無効な指数データ:', index)
      }
      return isValid
    })

    if (validIndices.length === 0) {
      console.warn('IndexChart: 有効な指数データが見つかりません', indicesData)
      return
    }

    console.log('IndexChart: 有効な指数データ数:', validIndices.length)
  } catch (error) {
    console.error('IndexChart: データ処理エラー:', error)
    return
  }

  try {
    const option = {
      title: {
        text: '市場指数データ',
        left: 'center',
        textStyle: {
          fontSize: 16,
          fontWeight: 'bold'
        }
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
        let result = params[0].name + '<br/>'
        params.forEach(param => {
          const value = param.value
          const change = param.data.change || 0
          const changePercent = param.data.changePercent || 0
          const changeColor = change >= 0 ? '#22c55e' : '#ef4444'
          
          result += `
            <div style="display: flex; align-items: center; margin: 4px 0;">
              <span style="display: inline-block; width: 10px; height: 10px; background-color: ${param.color}; border-radius: 50%; margin-right: 8px;"></span>
              <span style="font-weight: bold;">${param.seriesName}:</span>
              <span style="margin-left: 8px;">${value.toLocaleString()}</span>
              <span style="margin-left: 8px; color: ${changeColor};">
                ${change >= 0 ? '+' : ''}${change.toFixed(2)} (${changePercent >= 0 ? '+' : ''}${changePercent.toFixed(2)}%)
              </span>
            </div>
          `
        })
        return result
      }
    },
    legend: {
      top: 30,
      left: 'center',
      type: 'scroll'
    },
    grid: {
      left: '10%',
      right: '10%',
      bottom: '15%',
      top: '20%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: validIndices[0]?.dates || [],
      axisLabel: {
        formatter: function(value) {
          const date = new Date(value)
          return `${date.getMonth() + 1}/${date.getDate()}`
        }
      }
    },
    yAxis: {
      type: 'value',
      scale: true,
      axisLabel: {
        formatter: function(value) {
          return value.toLocaleString()
        }
      },
      splitLine: {
        show: true,
        lineStyle: {
          type: 'dashed',
          opacity: 0.5
        }
      }
    },
    series: validIndices.map((index, i) => {
      const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
      const color = colors[i % colors.length]
      
      // データの安全な処理
      const seriesData = (index.dates || []).map((date, j) => ({
        value: index.values?.[j] || 0,
        change: index.changes?.[j] || 0,
        changePercent: index.changePercent?.[j] || 0
      }))
      
      return {
        name: index.name || `指数${i + 1}`,
        type: 'line',
        smooth: true,
        symbol: 'circle',
        symbolSize: 6,
        lineStyle: {
          width: 2,
          color: color
        },
        itemStyle: {
          color: color,
          borderColor: '#fff',
          borderWidth: 2
        },
        areaStyle: {
          opacity: 0.1,
          color: color
        },
        emphasis: {
          focus: 'series',
          lineStyle: {
            width: 3
          },
          itemStyle: {
            borderWidth: 3,
            shadowBlur: 10,
            shadowColor: color
          }
        },
        data: seriesData
      }
    })
  }

  chartInstance.setOption(option, true)
  console.log('IndexChart: チャート更新完了')
  } catch (error) {
    console.error('IndexChart: チャート描画エラー:', error)
  }
}

const resizeChart = () => {
  if (chartInstance) {
    chartInstance.resize()
  }
}

onMounted(() => {
  initChart()
  window.addEventListener('resize', resizeChart)
})

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.dispose()
  }
  window.removeEventListener('resize', resizeChart)
})

watch(() => props.indexData, updateChart, { deep: true })
watch(() => props.period, updateChart)
</script>

<style scoped>
.index-chart-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.chart-container {
  width: 100%;
  height: 100%;
  min-height: 300px;
}
</style>
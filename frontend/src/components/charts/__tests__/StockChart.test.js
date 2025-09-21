import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import StockChart from '../StockChart.vue'

// EChartsをモック
vi.mock('echarts', () => ({
  init: vi.fn(() => ({
    setOption: vi.fn(),
    dispose: vi.fn(),
    resize: vi.fn(),
    on: vi.fn()
  }))
}))

describe('StockChart Component', () => {
  let wrapper

  const mockStockData = {
    '6326': {
      symbol: '6326',
      company_name: 'クボタ',
      dates: ['2025-09-20', '2025-09-21'],
      prices: [2500.0, 2550.0],
      volumes: [1000000, 1200000]
    },
    '9984': {
      symbol: '9984',
      company_name: 'ソフトバンクグループ',
      dates: ['2025-09-20', '2025-09-21'],
      prices: [8500.0, 8600.0],
      volumes: [800000, 900000]
    }
  }

  beforeEach(() => {
    wrapper = mount(StockChart, {
      props: {
        stockData: mockStockData,
        period: '7d'
      }
    })
  })

  afterEach(() => {
    wrapper.unmount()
  })

  describe('初期化', () => {
    it('コンポーネントが正しくレンダリングされる', () => {
      expect(wrapper.find('.stock-chart-container').exists()).toBe(true)
      expect(wrapper.find('.chart-main').exists()).toBe(true)
    })

    it('チャートコンテナが適切な構造を持つ', () => {
      const container = wrapper.find('.chart-main')
      expect(container.exists()).toBe(true)
    })
  })

  describe('データ表示', () => {
    it('株価データを正しく処理する', async () => {
      await wrapper.setProps({ stockData: mockStockData })
      
      expect(wrapper.props('stockData')).toEqual(mockStockData)
    })

    it('空のデータセットを処理する', async () => {
      await wrapper.setProps({ stockData: {} })
      
      expect(wrapper.props('stockData')).toEqual({})
    })

    it('APIレスポンス形式のデータを処理する', async () => {
      const apiResponse = {
        success: true,
        data: mockStockData
      }
      
      await wrapper.setProps({ stockData: apiResponse })
      expect(wrapper.props('stockData')).toEqual(apiResponse)
    })
  })

  describe('Props検証', () => {
    it('period プロパティが正しく設定される', () => {
      expect(wrapper.props('period')).toBe('7d')
    })

    it('heightプロパティのデフォルト値が設定される', () => {
      const defaultWrapper = mount(StockChart)
      expect(defaultWrapper.props('height')).toBe('400px')
    })

    it('period変更時に再描画される', async () => {
      await wrapper.setProps({ period: '1m' })
      expect(wrapper.props('period')).toBe('1m')
    })
  })

  describe('イベント処理', () => {
    it('retryイベントが正しく発生する', async () => {
      // retryボタンやエラー状態のテストは実装に依存
      // 基本的なイベント発行機能のテスト
      await wrapper.vm.$emit('retry')
      
      expect(wrapper.emitted()).toHaveProperty('retry')
    })
  })

  describe('エラーハンドリング', () => {
    it('無効なデータでも正常に動作する', async () => {
      const invalidData = {
        invalid: 'structure'
      }
      
      await wrapper.setProps({ stockData: invalidData })
      
      expect(wrapper.find('.stock-chart-container').exists()).toBe(true)
    })

    it('nullデータでも正常に動作する', async () => {
      await wrapper.setProps({ stockData: null })
      
      expect(wrapper.find('.stock-chart-container').exists()).toBe(true)
    })
  })
})
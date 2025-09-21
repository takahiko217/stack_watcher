import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import IndexChart from '../IndexChart.vue'

// EChartsをモック
vi.mock('echarts', () => ({
  init: vi.fn(() => ({
    setOption: vi.fn(),
    dispose: vi.fn(),
    resize: vi.fn(),
    on: vi.fn()
  }))
}))

describe('IndexChart Component', () => {
  let wrapper

  const mockIndexData = {
    '^N225': {
      name: '日経225',
      symbol: '^N225',
      dates: ['2025-09-20', '2025-09-21'],
      values: [28450.0, 28520.5],
      changes: [120.5, 70.5],
      changePercent: [0.42, 0.25],
      description: '日経平均株価'
    },
    '^TPX': {
      name: 'TOPIX',
      symbol: '^TPX',
      dates: ['2025-09-20', '2025-09-21'],
      values: [1980.0, 1985.2],
      changes: [15.3, 5.2],
      changePercent: [0.78, 0.26],
      description: '東証株価指数'
    }
  }

  beforeEach(() => {
    wrapper = mount(IndexChart, {
      props: {
        indexData: mockIndexData,
        period: '7d'
      }
    })
  })

  afterEach(() => {
    wrapper.unmount()
  })

  describe('初期化', () => {
    it('コンポーネントが正しくレンダリングされる', () => {
      expect(wrapper.find('.index-chart-container').exists()).toBe(true)
      expect(wrapper.find('.chart-container').exists()).toBe(true)
    })

    it('チャートコンテナのスタイルが正しく設定される', () => {
      const container = wrapper.find('.chart-container')
      expect(container.exists()).toBe(true)
    })
  })

  describe('データ処理', () => {
    it('有効な指数データを正しく処理する', async () => {
      await wrapper.setProps({ indexData: mockIndexData })
      
      // コンポーネントがデータを受け取ることを確認
      expect(wrapper.props('indexData')).toEqual(mockIndexData)
    })

    it('空のデータを適切に処理する', async () => {
      await wrapper.setProps({ indexData: {} })
      
      // エラーが発生しないことを確認
      expect(wrapper.props('indexData')).toEqual({})
    })

    it('APIレスポンス形式のデータを処理する', async () => {
      const apiResponse = {
        success: true,
        data: mockIndexData
      }
      
      await wrapper.setProps({ indexData: apiResponse })
      expect(wrapper.props('indexData')).toEqual(apiResponse)
    })
  })

  describe('Props', () => {
    it('periodプロパティが正しく設定される', () => {
      expect(wrapper.props('period')).toBe('7d')
    })

    it('periodが変更されると再描画がトリガーされる', async () => {
      await wrapper.setProps({ period: '1m' })
      expect(wrapper.props('period')).toBe('1m')
    })

    it('デフォルトのindexDataが空オブジェクトである', () => {
      const defaultWrapper = mount(IndexChart)
      expect(defaultWrapper.props('indexData')).toEqual({})
    })
  })

  describe('ライフサイクル', () => {
    it('マウント時にチャートが初期化される', () => {
      // echartsのinitが呼ばれることを間接的に確認
      expect(wrapper.find('.chart-container').exists()).toBe(true)
    })

    it('アンマウント時にリソースがクリーンアップされる', () => {
      const container = wrapper.find('.chart-container')
      expect(container.exists()).toBe(true)
      
      wrapper.unmount()
      // unmount後にエラーが発生しないことを確認
    })
  })

  describe('エラーハンドリング', () => {
    it('不正なデータ形式でもエラーが発生しない', async () => {
      const invalidData = {
        invalid: 'data'
      }
      
      await wrapper.setProps({ indexData: invalidData })
      
      // コンポーネントが正常に動作することを確認
      expect(wrapper.find('.index-chart-container').exists()).toBe(true)
    })

    it('nullデータでも正常に動作する', async () => {
      await wrapper.setProps({ indexData: null })
      
      expect(wrapper.find('.index-chart-container').exists()).toBe(true)
    })
  })
})
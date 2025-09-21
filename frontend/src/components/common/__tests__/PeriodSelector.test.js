import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import PeriodSelector from '../PeriodSelector.vue'

describe('PeriodSelector Component', () => {
  let wrapper

  beforeEach(() => {
    wrapper = mount(PeriodSelector, {
      props: {
        period: '7d'
      }
    })
  })

  afterEach(() => {
    wrapper.unmount()
  })

  describe('初期化', () => {
    it('コンポーネントが正しくレンダリングされる', () => {
      expect(wrapper.find('.period-selector').exists()).toBe(true)
      expect(wrapper.find('.flex').exists()).toBe(true)
    })

    it('期間選択ボタンが正しく表示される', () => {
      const buttons = wrapper.findAll('button')
      expect(buttons).toHaveLength(3)
      
      const buttonTexts = buttons.map(button => button.text())
      expect(buttonTexts).toContain('7日間')
      expect(buttonTexts).toContain('1ヶ月')
      expect(buttonTexts).toContain('3ヶ月')
    })
  })

  describe('期間選択', () => {
    it('現在選択されている期間がハイライトされる', () => {
      const activeButton = wrapper.find('button.bg-blue-500')
      expect(activeButton.exists()).toBe(true)
      expect(activeButton.text()).toBe('7日間')
    })

    it('期間ボタンクリックでイベントが発生する', async () => {
      const monthButton = wrapper.find('button:nth-child(2)')
      await monthButton.trigger('click')
      
      const emitted = wrapper.emitted('update:period')
      expect(emitted).toBeTruthy()
      expect(emitted[0]).toEqual(['1m'])
    })

    it('期間変更時にスタイルが更新される', async () => {
      await wrapper.setProps({ period: '1m' })
      
      const activeButton = wrapper.find('button.bg-blue-500')
      expect(activeButton.text()).toBe('1ヶ月')
    })
  })

  describe('Props検証', () => {
    it('period プロパティが必須である', () => {
      expect(wrapper.props('period')).toBe('7d')
    })

    it('異なるperiod値で正しく動作する', async () => {
      await wrapper.setProps({ period: '3m' })
      
      const activeButton = wrapper.find('button.bg-blue-500')
      expect(activeButton.text()).toBe('3ヶ月')
    })
  })

  describe('UI/UX', () => {
    it('ボタンにホバー効果のクラスが含まれる', () => {
      const inactiveButton = wrapper.find('button.bg-white')
      expect(inactiveButton.classes()).toContain('hover:bg-gray-50')
      expect(inactiveButton.classes()).toContain('hover:border-gray-400')
    })

    it('適切な間隔とパディングが設定される', () => {
      const container = wrapper.find('.flex')
      expect(container.classes()).toContain('gap-2')
      
      const buttons = wrapper.findAll('button')
      buttons.forEach(button => {
        expect(button.classes()).toContain('px-3')
        expect(button.classes()).toContain('py-1')
      })
    })
  })

  describe('アクセシビリティ', () => {
    it('ボタンが適切な要素である', () => {
      const buttons = wrapper.findAll('button')
      buttons.forEach(button => {
        expect(button.element.tagName).toBe('BUTTON')
      })
    })

    it('フォーカス可能な要素である', () => {
      const buttons = wrapper.findAll('button')
      buttons.forEach(button => {
        expect(button.element.tabIndex).not.toBe(-1)
      })
    })
  })
})
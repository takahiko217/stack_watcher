import { test, expect } from '@playwright/test'

test.describe('Stack Watcher Dashboard E2E', () => {
  test.beforeEach(async ({ page }) => {
    // バックエンドが起動していることを確認
    await page.goto('/')
    await page.waitForLoadState('networkidle')
  })

  test('ダッシュボードが正常に表示される', async ({ page }) => {
    // ページタイトルの確認
    await expect(page).toHaveTitle(/Stack Watcher/)
    
    // ヘッダーの確認
    await expect(page.locator('h1')).toContainText('Stack Watcher Dashboard')
    
    // サブタイトルの確認
    await expect(page.locator('p')).toContainText('株価・指数・気象データの統合監視')
  })

  test('期間選択機能が動作する', async ({ page }) => {
    // 期間選択セクションが表示されることを確認
    const periodSelector = page.locator('.period-selector-section')
    await expect(periodSelector).toBeVisible()
    
    // 期間選択ボタンが表示されることを確認
    const buttons = page.locator('.period-selector button')
    await expect(buttons).toHaveCount(3)
    
    // デフォルトで「7日間」が選択されていることを確認
    const activeButton = page.locator('button.bg-blue-500')
    await expect(activeButton).toContainText('7日間')
    
    // 「1ヶ月」を選択
    const monthButton = page.locator('button:has-text("1ヶ月")')
    await monthButton.click()
    
    // 選択が変更されることを確認
    await expect(monthButton).toHaveClass(/bg-blue-500/)
    
    // ページが再読み込みされることを確認（ネットワーク活動）
    await page.waitForLoadState('networkidle')
  })

  test('株価チャートが表示される', async ({ page }) => {
    // 株価チャートセクションの確認
    const stockChart = page.locator('.chart-card').first()
    await expect(stockChart).toBeVisible()
    
    // チャートタイトルの確認
    await expect(stockChart.locator('h3, .chart-title')).toBeVisible()
    
    // 銘柄凡例の確認
    const legends = stockChart.locator('.legend-item, .chart-legend')
    if (await legends.count() > 0) {
      await expect(legends.first()).toBeVisible()
    }
  })

  test('指数チャートが表示される', async ({ page }) => {
    // 指数チャートセクションの確認（2番目のチャート）
    const indexChart = page.locator('.chart-card').nth(1)
    await expect(indexChart).toBeVisible()
    
    // チャートが読み込まれるまで待機
    await page.waitForTimeout(3000)
    
    // チャートコンテナが存在することを確認
    const chartContainer = indexChart.locator('.chart-container, .index-chart-container')
    await expect(chartContainer).toBeVisible()
  })

  test('気象チャートが表示される', async ({ page }) => {
    // 気象チャートセクションの確認（3番目のチャート）
    const weatherChart = page.locator('.chart-card').nth(2)
    await expect(weatherChart).toBeVisible()
    
    // チャートが読み込まれるまで待機
    await page.waitForTimeout(3000)
    
    // チャートコンテナが存在することを確認
    const chartContainer = weatherChart.locator('.chart-container, .weather-chart-container')
    await expect(chartContainer).toBeVisible()
  })

  test('API テストセクションが動作する', async ({ page }) => {
    // API テストセクションまでスクロール
    const apiSection = page.locator('.api-test-section')
    await apiSection.scrollIntoViewIfNeeded()
    await expect(apiSection).toBeVisible()
    
    // 株価API テストボタンをクリック
    const stockApiButton = page.locator('button:has-text("株価API テスト")')
    await stockApiButton.click()
    
    // 結果が表示されるまで待機
    await page.waitForTimeout(5000)
    
    // 結果セクションが表示されることを確認
    const resultSection = page.locator('.api-result')
    await expect(resultSection).toBeVisible()
    
    // 結果コンテンツが表示されることを確認
    const resultContent = page.locator('.result-content')
    await expect(resultContent).toBeVisible()
    await expect(resultContent).not.toBeEmpty()
  })

  test('レスポンシブデザインの確認', async ({ page }) => {
    // デスクトップサイズで開始
    await page.setViewportSize({ width: 1024, height: 768 })
    
    // チャートが3つ表示されることを確認
    const charts = page.locator('.chart-card')
    await expect(charts).toHaveCount(3)
    
    // タブレットサイズに変更
    await page.setViewportSize({ width: 768, height: 1024 })
    await page.waitForTimeout(1000)
    
    // チャートが依然として表示されることを確認
    await expect(charts).toHaveCount(3)
    
    // モバイルサイズに変更
    await page.setViewportSize({ width: 375, height: 667 })
    await page.waitForTimeout(1000)
    
    // チャートが依然として表示されることを確認
    await expect(charts).toHaveCount(3)
  })

  test('エラーハンドリングの確認', async ({ page }) => {
    // バックエンドが停止している場合のシミュレーションは困難なため、
    // 基本的なエラー表示要素の存在確認のみ行う
    
    // ページが正常に読み込まれることを確認
    await expect(page.locator('body')).toBeVisible()
    
    // エラー状態でも基本レイアウトが崩れないことを確認
    const container = page.locator('.dashboard-container')
    await expect(container).toBeVisible()
  })

  test('パフォーマンステスト', async ({ page }) => {
    // ページ読み込み時間の測定
    const startTime = Date.now()
    
    await page.goto('/')
    await page.waitForLoadState('networkidle')
    
    const loadTime = Date.now() - startTime
    
    // 10秒以内に読み込まれることを確認
    expect(loadTime).toBeLessThan(10000)
    
    console.log(`ページ読み込み時間: ${loadTime}ms`)
  })
})
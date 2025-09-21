<template>
  <div class="period-selector">
    <!-- 期間選択タブ -->
    <div class="flex bg-gray-100 rounded-lg p-1 space-x-1">
      <button
        v-for="option in periodOptions"
        :key="option.value"
        @click="selectPeriod(option.value)"
        :class="[
          'px-4 py-2 rounded-md text-sm font-medium transition-all duration-200',
          selectedPeriod === option.value
            ? 'bg-white text-blue-600 shadow-sm'
            : 'text-gray-600 hover:text-gray-800 hover:bg-gray-50'
        ]"
        :disabled="isLoading"
      >
        {{ option.label }}
      </button>
    </div>
    
    <!-- ローディング表示 -->
    <div
      v-if="isLoading"
      class="ml-3 flex items-center text-sm text-gray-500"
    >
      <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      データ更新中...
    </div>
    
    <!-- エラー表示 -->
    <div
      v-if="error"
      class="ml-3 flex items-center text-sm text-red-500"
    >
      <svg class="mr-1 h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
      </svg>
      エラーが発生しました
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useSyncStore } from '../stores/syncStore'
import { useStockStore } from '../stores/stockStore'
import { useIndexStore } from '../stores/indexStore'
import { useWeatherStore } from '../stores/weatherStore'

export default {
  name: 'PeriodSelector',
  setup() {
    const syncStore = useSyncStore()
    const stockStore = useStockStore()
    const indexStore = useIndexStore()
    const weatherStore = useWeatherStore()

    // 期間オプション
    const periodOptions = [
      { value: '7d', label: '7日間' },
      { value: '1m', label: '1ヶ月' },
      { value: '3m', label: '四半期' }
    ]

    // 現在選択中の期間
    const selectedPeriod = computed(() => syncStore.globalPeriod)

    // ローディング状態（いずれかのStoreがローディング中）
    const isLoading = computed(() => {
      return stockStore.isLoading || indexStore.isLoading || weatherStore.isLoading
    })

    // エラー状態（いずれかのStoreでエラー）
    const error = computed(() => {
      return stockStore.error || indexStore.error || weatherStore.error
    })

    // 期間選択処理
    const selectPeriod = (period) => {
      if (isLoading.value) return
      
      console.log('Period selected:', period)
      // 同期Storeを通じて全Store の期間を変更
      syncStore.setPeriod(period)
    }

    return {
      periodOptions,
      selectedPeriod,
      isLoading,
      error,
      selectPeriod
    }
  }
}
</script>

<style scoped>
.period-selector {
  @apply flex items-center;
}

/* タブのホバーエフェクト */
.period-selector button:hover {
  transform: translateY(-1px);
}

/* アクティブタブの特別なスタイル */
.period-selector button:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* レスポンシブ対応 */
@media (max-width: 640px) {
  .period-selector {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .period-selector .flex {
    width: 100%;
  }
  
  .period-selector button {
    flex: 1;
  }
}
</style>
<template>
  <div class="period-selector">
    <div class="flex flex-wrap gap-2">
      <button
        v-for="option in periodOptions"
        :key="option.value"
        @click="$emit('update:period', option.value)"
        :class="[
          'px-3 py-1 text-sm font-medium rounded-md border transition-all duration-200',
          period === option.value
            ? 'bg-blue-500 text-white border-blue-500 shadow-md'
            : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50 hover:border-gray-400'
        ]"
      >
        {{ option.label }}
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  period: {
    type: String,
    required: true
  }
})

defineEmits(['update:period'])

const periodOptions = [
  { value: '7d', label: '7日間' },
  { value: '1m', label: '1ヶ月' },
  { value: '3m', label: '3ヶ月' }
]
</script>

<style scoped>
.period-selector {
  padding: 10px 0;
}
</style>
<template>
  <div id="app">
    <h1>Hello World!</h1>
    <p>Vue.js + FastAPI アプリケーションが正常に動作しています。</p>
    <button @click="count++">クリック回数: {{ count }}</button>
    
    <div class="api-test">
      <h2>API 通信テスト</h2>
      <button @click="testHelloAPI">Hello API テスト</button>
      <button @click="testHealthAPI">Health API テスト</button>
      <div v-if="apiResponse" class="response">
        <h3>レスポンス:</h3>
        <pre>{{ apiResponse }}</pre>
      </div>
      <div v-if="apiError" class="error">
        <h3>エラー:</h3>
        <pre>{{ apiError }}</pre>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'App',
  setup() {
    const count = ref(0)
    const apiResponse = ref(null)
    const apiError = ref(null)

    const testHelloAPI = async () => {
      try {
        apiError.value = null
        const response = await fetch('/api/hello')
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`)
        }
        const data = await response.json()
        apiResponse.value = JSON.stringify(data, null, 2)
      } catch (error) {
        apiError.value = error.message
        apiResponse.value = null
      }
    }

    const testHealthAPI = async () => {
      try {
        apiError.value = null
        const response = await fetch('/health')
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`)
        }
        const data = await response.json()
        apiResponse.value = JSON.stringify(data, null, 2)
      } catch (error) {
        apiError.value = error.message
        apiResponse.value = null
      }
    }

    return {
      count,
      apiResponse,
      apiError,
      testHelloAPI,
      testHealthAPI
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin: 5px;
}

button:hover {
  background-color: #369870;
}

.api-test {
  margin-top: 40px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.response {
  margin-top: 20px;
  text-align: left;
}

.response pre {
  background-color: #f5f5f5;
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
}

.error {
  margin-top: 20px;
  text-align: left;
}

.error pre {
  background-color: #ffe6e6;
  color: #d63031;
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
}
</style>

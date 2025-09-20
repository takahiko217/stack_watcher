/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // 株価チャート用カラー
        'stock-kubota': '#2563eb',      // 青 - クボタ
        'stock-softbank': '#dc2626',    // 赤 - ソフトバンク
        'stock-sakata': '#059669',      // 緑 - サカタのタネ
        
        // システムカラー
        'primary': '#1e40af',
        'secondary': '#6b7280',
        'success': '#059669',
        'warning': '#ea580c',
        'error': '#dc2626',
      }
    },
  },
  plugins: [],
}
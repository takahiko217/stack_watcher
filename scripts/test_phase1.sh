#!/bin/bash

echo "=== Stack Watcher Phase 1 MVP テスト ==="
echo ""

API_BASE="http://localhost:8003/api/v1"
EXPECTED_SYMBOLS=("6326" "9984" "1377")
EXPECTED_COMPANIES=("クボタ" "ソフトバンクグループ" "サカタのタネ")

# 色付き出力用
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

pass_count=0
total_tests=0

# テスト結果記録関数
test_result() {
    total_tests=$((total_tests + 1))
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ PASS${NC}: $2"
        pass_count=$((pass_count + 1))
    else
        echo -e "${RED}❌ FAIL${NC}: $2"
    fi
}

echo -e "${BLUE}1. バックエンドAPIテスト${NC}"
echo "-----------------------------------"

# ヘルスチェック
echo "🔍 ヘルスチェック実行中..."
health_status=$(curl -s -o /dev/null -w "%{http_code}" "$API_BASE/../health")
if [ "$health_status" = "200" ]; then
    test_result 0 "ヘルスチェック"
else
    test_result 1 "ヘルスチェック (HTTP $health_status)"
fi

# 銘柄一覧取得
echo "🔍 銘柄一覧取得テスト実行中..."
symbols_response=$(curl -s "$API_BASE/stocks/symbols")
symbols_count=$(echo "$symbols_response" | jq -r '.data.symbols | length' 2>/dev/null)

if [ "$symbols_count" = "3" ]; then
    test_result 0 "銘柄一覧取得 (3銘柄)"
else
    test_result 1 "銘柄一覧取得 (期待値: 3, 実際: $symbols_count)"
fi

# 各銘柄のテスト
echo ""
echo -e "${BLUE}2. 株価データ取得テスト${NC}"
echo "-----------------------------------"

for i in "${!EXPECTED_SYMBOLS[@]}"; do
    symbol="${EXPECTED_SYMBOLS[$i]}"
    company="${EXPECTED_COMPANIES[$i]}"
    
    echo "🔍 $symbol ($company) テスト実行中..."
    
    # 7日間データ取得
    stock_response=$(curl -s "$API_BASE/stocks?symbols=$symbol&period=7d")
    
    # レスポンス成功チェック
    success=$(echo "$stock_response" | jq -r '.success' 2>/dev/null)
    if [ "$success" = "true" ]; then
        test_result 0 "$symbol API成功レスポンス"
    else
        test_result 1 "$symbol API失敗"
        continue
    fi
    
    # データ存在チェック
    stocks_count=$(echo "$stock_response" | jq -r '.data.stocks | length' 2>/dev/null)
    if [ "$stocks_count" = "1" ]; then
        test_result 0 "$symbol データ存在"
    else
        test_result 1 "$symbol データなし"
        continue
    fi
    
    # データポイント数チェック（7日間）
    data_points=$(echo "$stock_response" | jq -r '.data.stocks[0].data_points | length' 2>/dev/null)
    if [ "$data_points" -ge "5" ] && [ "$data_points" -le "7" ]; then
        test_result 0 "$symbol データポイント数 ($data_points 日分)"
    else
        test_result 1 "$symbol データポイント数異常 ($data_points 日分)"
    fi
    
    # 最新価格チェック
    latest_price=$(echo "$stock_response" | jq -r '.data.stocks[0].data_points[-1].close' 2>/dev/null)
    if [ "$latest_price" != "null" ] && [ "$latest_price" != "" ]; then
        test_result 0 "$symbol 最新価格取得 (¥$latest_price)"
    else
        test_result 1 "$symbol 最新価格取得失敗"
    fi
done

# 複数銘柄同時取得テスト
echo ""
echo -e "${BLUE}3. 複数銘柄同時取得テスト${NC}"
echo "-----------------------------------"

echo "🔍 3銘柄同時取得テスト実行中..."
multi_response=$(curl -s "$API_BASE/stocks?symbols=6326,9984,1377&period=7d")
multi_success=$(echo "$multi_response" | jq -r '.success' 2>/dev/null)
multi_count=$(echo "$multi_response" | jq -r '.data.stocks | length' 2>/dev/null)

if [ "$multi_success" = "true" ] && [ "$multi_count" = "3" ]; then
    test_result 0 "3銘柄同時取得"
else
    test_result 1 "3銘柄同時取得 (成功: $multi_success, 銘柄数: $multi_count)"
fi

# データ形式チェック
echo ""
echo -e "${BLUE}4. データ形式チェック${NC}"
echo "-----------------------------------"

echo "🔍 データ形式確認中..."
sample_data=$(echo "$multi_response" | jq -r '.data.stocks[0].data_points[0]' 2>/dev/null)

# 必要フィールドの存在確認
required_fields=("date" "open" "high" "low" "close" "volume")
for field in "${required_fields[@]}"; do
    field_value=$(echo "$sample_data" | jq -r ".$field" 2>/dev/null)
    if [ "$field_value" != "null" ] && [ "$field_value" != "" ]; then
        test_result 0 "データフィールド '$field' 存在"
    else
        test_result 1 "データフィールド '$field' 不足"
    fi
done

# 結果サマリー
echo ""
echo "======================================="
echo -e "${BLUE}Phase 1 MVP テスト結果サマリー${NC}"
echo "======================================="

if [ $pass_count -eq $total_tests ]; then
    echo -e "${GREEN}🎉 全テスト合格!${NC}"
    echo -e "${GREEN}Phase 1 MVP要件を満たしています${NC}"
    echo ""
    echo "✅ 基本的なグラフ表示機能: API準備完了"
    echo "✅ 3銘柄の株価表示: クボタ、ソフトバンクグループ、サカタのタネ対応"
    echo "✅ 7日間の時間軸: データ取得確認済み"
else
    echo -e "${YELLOW}⚠️ 一部テスト失敗${NC}"
    echo -e "合格: ${GREEN}$pass_count${NC}/$total_tests"
fi

echo ""
echo "詳細な株価データサンプル:"
echo "$multi_response" | jq '.data.stocks[] | {symbol: .symbol, company: .company_name, latest_price: .data_points[-1].close, data_points: (.data_points | length)}' 2>/dev/null

exit $((total_tests - pass_count))
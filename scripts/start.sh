#!/bin/bash

# Stack Watcher アプリケーション起動スクリプト
# 
# このスクリプトはフロントエンドとバックエンドを同時に起動します。
# 初心者向けに各ステップを詳しく説明しています。

echo "🚀 Stack Watcher アプリケーションを起動しています..."
echo ""

# スクリプトが実行されているディレクトリを取得
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# プロジェクトルートディレクトリに移動
cd "$PROJECT_ROOT"

echo "📁 プロジェクトディレクトリ: $PROJECT_ROOT"
echo ""

# 必要なファイルの存在確認
echo "🔍 必要なファイルの確認中..."

# フロントエンドの確認
if [ ! -d "frontend/node_modules" ]; then
    echo "❌ フロントエンドの依存関係がインストールされていません"
    echo "   ./scripts/setup.sh を先に実行してください"
    exit 1
fi

# バックエンドの確認
if [ ! -d "backend/venv" ]; then
    echo "❌ バックエンドの仮想環境が作成されていません"
    echo "   ./scripts/setup.sh を先に実行してください"
    exit 1
fi

echo "✅ 必要なファイルが確認されました"
echo ""

# 他のプロセスが既に起動しているかチェック
echo "🔍 ポートの使用状況を確認中..."

# ポート3000と8000の確認
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  ポート3000は既に使用されています"
    echo "   既存のプロセスを停止してから再実行してください"
fi

if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  ポート8000は既に使用されています"
    echo "   既存のプロセスを停止してから再実行してください"
fi

echo "✅ ポートの確認が完了しました"
echo ""

# バックエンドの起動
echo "🐍 バックエンドサーバーを起動中..."
cd "$PROJECT_ROOT/backend"

# 仮想環境をアクティベート
source venv/bin/activate

# バックエンドをバックグラウンドで起動
echo "   FastAPI サーバーを起動します (ポート: 8000)..."
python main.py &
BACKEND_PID=$!

# バックエンドの起動を少し待つ
sleep 3

# バックエンドが正常に起動したかチェック
if ps -p $BACKEND_PID > /dev/null; then
    echo "✅ バックエンドサーバーが起動しました (PID: $BACKEND_PID)"
else
    echo "❌ バックエンドサーバーの起動に失敗しました"
    exit 1
fi

echo ""

# フロントエンドの起動
echo "⚡ フロントエンドサーバーを起動中..."
cd "$PROJECT_ROOT/frontend"

echo "   Vue.js 開発サーバーを起動します (ポート: 3000)..."
npm run dev &
FRONTEND_PID=$!

# フロントエンドの起動を少し待つ
sleep 3

# フロントエンドが正常に起動したかチェック
if ps -p $FRONTEND_PID > /dev/null; then
    echo "✅ フロントエンドサーバーが起動しました (PID: $FRONTEND_PID)"
else
    echo "❌ フロントエンドサーバーの起動に失敗しました"
    # バックエンドも停止
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo ""

# 起動完了メッセージ
echo "🎉 Stack Watcher が正常に起動しました！"
echo ""
echo "📋 アクセス情報:"
echo "   🌐 フロントエンド: http://localhost:3000"
echo "   🔗 バックエンドAPI: http://localhost:8000"
echo "   📖 API文書: http://localhost:8000/docs"
echo ""
echo "💡 使用方法:"
echo "   - ブラウザで http://localhost:3000 にアクセスしてください"
echo "   - コードを変更すると自動でリロードされます"
echo "   - 停止するには Ctrl+C を押してください"
echo ""
echo "🔧 プロセス情報:"
echo "   - バックエンド PID: $BACKEND_PID"
echo "   - フロントエンド PID: $FRONTEND_PID"
echo ""

# 終了時のクリーンアップ関数
cleanup() {
    echo ""
    echo "🛑 アプリケーションを停止中..."
    
    # フロントエンドプロセスを停止
    if ps -p $FRONTEND_PID > /dev/null; then
        echo "   フロントエンドサーバーを停止します..."
        kill $FRONTEND_PID 2>/dev/null
    fi
    
    # バックエンドプロセスを停止
    if ps -p $BACKEND_PID > /dev/null; then
        echo "   バックエンドサーバーを停止します..."
        kill $BACKEND_PID 2>/dev/null
    fi
    
    echo "✅ すべてのサーバーが停止しました"
    echo "👋 お疲れさまでした！"
    exit 0
}

# Ctrl+C を押された時にクリーンアップ関数を実行
trap cleanup SIGINT SIGTERM

# プロセスが終了するまで待機
wait
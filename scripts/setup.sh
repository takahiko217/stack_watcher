#!/bin/bash

# Stack Watcher 環境セットアップスクリプト
# 
# このスクリプトは開発環境を自動でセットアップします。
# 初心者向けに各ステップを詳しく説明しています。

echo "🚀 Stack Watcher 環境セットアップを開始します..."
echo ""

# スクリプトが実行されているディレクトリを取得
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# プロジェクトルートディレクトリに移動
cd "$PROJECT_ROOT"

echo "📁 プロジェクトディレクトリ: $PROJECT_ROOT"
echo ""

# Node.js と npm の確認
echo "🔍 Node.js と npm の確認..."
if command -v node >/dev/null 2>&1; then
    echo "✅ Node.js がインストールされています: $(node --version)"
else
    echo "❌ Node.js がインストールされていません"
    echo "   https://nodejs.org/ からダウンロードしてインストールしてください"
    exit 1
fi

if command -v npm >/dev/null 2>&1; then
    echo "✅ npm がインストールされています: $(npm --version)"
else
    echo "❌ npm がインストールされていません"
    exit 1
fi

echo ""

# Python の確認
echo "🐍 Python の確認..."
if command -v python3 >/dev/null 2>&1; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Python がインストールされています: $PYTHON_VERSION"
else
    echo "❌ Python3 がインストールされていません"
    echo "   https://www.python.org/ からダウンロードしてインストールしてください"
    exit 1
fi

echo ""

# フロントエンド依存関係のインストール
echo "📦 フロントエンド依存関係をインストール中..."
cd frontend

if [ -f "package.json" ]; then
    echo "   package.json が見つかりました"
    echo "   npm install を実行します..."
    
    if npm install; then
        echo "✅ フロントエンド依存関係のインストールが完了しました"
    else
        echo "❌ フロントエンド依存関係のインストールに失敗しました"
        exit 1
    fi
else
    echo "❌ package.json が見つかりません"
    exit 1
fi

echo ""

# バックエンドセットアップ
echo "🔧 バックエンド環境をセットアップ中..."
cd "$PROJECT_ROOT/backend"

# Python仮想環境の作成
echo "   Python仮想環境を作成します..."
if python3 -m venv venv; then
    echo "✅ 仮想環境の作成が完了しました"
else
    echo "❌ 仮想環境の作成に失敗しました"
    exit 1
fi

# 仮想環境をアクティベート
echo "   仮想環境をアクティベートします..."
source venv/bin/activate

# 依存関係のインストール
echo "   Python依存関係をインストールします..."
if [ -f "requirements.txt" ]; then
    if pip install -r requirements.txt; then
        echo "✅ バックエンド依存関係のインストールが完了しました"
    else
        echo "❌ バックエンド依存関係のインストールに失敗しました"
        exit 1
    fi
else
    echo "❌ requirements.txt が見つかりません"
    exit 1
fi

echo ""

# 環境設定ファイルの作成
echo "⚙️  環境設定ファイルを作成中..."
cd "$PROJECT_ROOT/backend"

if [ ! -f ".env" ]; then
    echo "   .env ファイルを作成します..."
    cat > .env << EOL
# Stack Watcher バックエンド設定
# 
# セキュリティに関する重要な設定値はここで管理します

# アプリケーション設定
APP_NAME=Stack Watcher
APP_VERSION=1.0.0
DEBUG=true

# データベース設定
DATABASE_URL=sqlite:///./stack_watcher.db

# セキュリティ設定（本番環境では必ず変更してください）
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS設定
ALLOWED_ORIGINS=http://localhost:3000

# ログ設定
LOG_LEVEL=INFO
EOL
    echo "✅ .env ファイルが作成されました"
    echo "   📝 注意: 本番環境では SECRET_KEY を必ず変更してください"
else
    echo "✅ .env ファイルは既に存在します"
fi

echo ""

# 成功メッセージ
echo "🎉 環境セットアップが完了しました！"
echo ""
echo "📋 次のステップ:"
echo "   1. アプリケーションを起動: ./scripts/start.sh"
echo "   2. ブラウザで http://localhost:3000 にアクセス"
echo "   3. API文書は http://localhost:8000/docs で確認できます"
echo ""
echo "💡 ヒント:"
echo "   - 開発中はコードの変更が自動で反映されます"
echo "   - ログは各ターミナルウィンドウで確認できます"
echo "   - 停止は Ctrl+C を押してください"
echo ""
echo "Happy coding! 🚀"
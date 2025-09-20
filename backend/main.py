"""
Stack Watcher FastAPI アプリケーションのメインファイル

このファイルはFastAPIアプリケーションの起動ポイントとなります。
初心者向けにコメントを豊富に含めています。
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# FastAPIアプリケーションインスタンスを作成
# title: APIのタイトル
# description: APIの説明
# version: APIのバージョン
app = FastAPI(
    title="Stack Watcher API",
    description="技術スタック監視システムのAPI",
    version="1.0.0"
)

# CORS（Cross-Origin Resource Sharing）設定
# フロントエンドからのリクエストを許可するために必要
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Vue.jsアプリのURL
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可
    allow_headers=["*"],  # すべてのヘッダーを許可
)

# ルートエンドポイント
# アプリケーションが正常に動作しているかを確認するためのシンプルなエンドポイント
@app.get("/")
async def read_root():
    """
    ルートエンドポイント
    
    Returns:
        dict: アプリケーションの基本情報
    """
    return {
        "message": "Stack Watcher API へようこそ！",
        "status": "正常に動作中",
        "version": "1.0.0"
    }

# ヘルスチェックエンドポイント
# システムの状態を確認するためのエンドポイント
@app.get("/health")
async def health_check():
    """
    ヘルスチェックエンドポイント
    
    Returns:
        dict: システムの健全性情報
    """
    return {
        "status": "healthy",
        "message": "システムは正常に動作しています"
    }

# アプリケーションの起動（開発用）
if __name__ == "__main__":
    import uvicorn
    # uvicornサーバーでアプリケーションを起動
    # host="0.0.0.0": すべてのネットワークインターフェースでリッスン
    # port=8000: ポート8000で起動
    # reload=True: ファイル変更時に自動リロード（開発時のみ使用）
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
import os
import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

# 株価データサービスをインポート
from .stock_service import stock_service

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# FastAPIアプリケーション作成
app = FastAPI(
    title="Stack Watcher API",
    description="株価比較ツール API",
    version="1.0.0"
)

# CORS設定（フロントエンドからのアクセスを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:5173", 
        "http://localhost:5174",  # 新しいポート追加
        "http://127.0.0.1:3000", 
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",   # 新しいポート追加
        "https://hello-world-2392551287759861.aws.databricksapps.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 株価API エンドポイント ---

@app.get("/api/v1/stocks/symbols")
async def get_available_symbols():
    """利用可能な銘柄一覧を取得"""
    try:
        symbols = stock_service.get_available_symbols()
        return {
            "success": True,
            "data": {"symbols": symbols},
            "message": "銘柄一覧を取得しました"
        }
    except Exception as e:
        logger.error(f"銘柄一覧取得エラー: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/stocks/{symbol}")
async def get_stock_data(symbol: str, period: Optional[str] = "7d"):
    """個別銘柄の株価データを取得"""
    try:
        data = stock_service.get_stock_data(symbol, period)
        return {
            "success": True,
            "data": data,
            "message": f"{symbol}の株価データを取得しました"
        }
    except ValueError as e:
        logger.warning(f"無効なリクエスト: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"株価データ取得エラー: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/stocks")
async def get_multiple_stocks(symbols: str, period: Optional[str] = "7d"):
    """複数銘柄の株価データを一括取得"""
    try:
        # カンマ区切りの文字列を配列に変換
        symbol_list = [s.strip() for s in symbols.split(",") if s.strip()]
        
        if not symbol_list:
            raise ValueError("銘柄コードが指定されていません")
        
        data = stock_service.get_multiple_stocks(symbol_list, period)
        return {
            "success": True,
            "data": data,
            "message": f"{len(symbol_list)}銘柄の株価データを取得しました"
        }
    except ValueError as e:
        logger.warning(f"無効なリクエスト: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"複数銘柄データ取得エラー: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# --- 既存のAPI エンドポイント ---
@app.get("/api/hello")
async def hello():
    logger.info("Accessed /api/hello")
    return {"message": "Hello from FastAPI!"}

@app.get("/health")
async def health_check():
    logger.info("Health check at /health")
    return {"status": "healthy"}

@app.get("/api/v1/health")
async def api_health_check():
    """APIヘルスチェック"""
    try:
        # 簡単なデータ取得テストを実行
        test_symbols = stock_service.get_available_symbols()
        
        return {
            "success": True,
            "data": {
                "status": "healthy",
                "version": "1.0.0",
                "available_symbols": len(test_symbols),
                "services": {
                    "yfinance": "available",
                    "api": "running"
                }
            },
            "message": "システムは正常に動作しています"
        }
    except Exception as e:
        logger.error(f"ヘルスチェック失敗: {e}")
        return {
            "success": False,
            "data": {
                "status": "unhealthy",
                "error": str(e)
            },
            "message": "システムに問題があります"
        }

@app.get("/api/v1/demo")
async def get_demo_data():
    """デモ用の全銘柄データを取得"""
    try:
        # デフォルト3銘柄のデータを取得
        symbols = ["6326", "9984", "1377"]
        data = stock_service.get_multiple_stocks(symbols, "7d")
        
        return {
            "success": True,
            "data": data,
            "message": "デモ用株価データを取得しました"
        }
    except Exception as e:
        logger.error(f"デモデータ取得エラー: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# --- Static Files Setup ---
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
os.makedirs(static_dir, exist_ok=True)

app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

# --- Catch-all for React Routes ---
@app.get("/{full_path:path}")
async def serve_react(full_path: str):
    index_html = os.path.join(static_dir, "index.html")
    if os.path.exists(index_html):
        logger.info(f"Serving React frontend for path: /{full_path}")
        return FileResponse(index_html)
    logger.error("Frontend not built. index.html missing.")
    raise HTTPException(
        status_code=404,
        detail="Frontend not built. Please run 'npm run build' first."
    )
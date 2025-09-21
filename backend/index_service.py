"""
インデックスデータサービス
日経225、TOPIX、マザーズ指数のデータを取得・処理するサービス
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IndexService:
    """インデックスデータの取得と処理を担当するサービスクラス"""
    
    # インデックス銘柄の定義
    INDEX_SYMBOLS = {
        "^N225": {
            "name": "日経225",
            "symbol": "^N225",
            "description": "日経平均株価"
        },
        "^TPX": {
            "name": "TOPIX",
            "symbol": "^TPX", 
            "description": "東証株価指数"
        },
        "2516.T": {
            "name": "マザーズ指数",
            "symbol": "2516.T",
            "description": "東証マザーズ指数"
        }
    }
    
    def __init__(self):
        """IndexServiceの初期化"""
        logger.info("IndexService初期化完了")
    
    def get_period_days(self, period: str) -> int:
        """期間文字列を日数に変換"""
        period_mapping = {
            "7d": 7,
            "1m": 30,
            "3m": 90
        }
        return period_mapping.get(period, 7)
    
    def calculate_changes(self, values: List[float]) -> tuple[List[float], List[float]]:
        """前日比と騰落率を計算"""
        if len(values) < 2:
            return [0.0] * len(values), [0.0] * len(values)
        
        changes = []
        change_percent = []
        
        for i in range(len(values)):
            if i == 0:
                changes.append(0.0)
                change_percent.append(0.0)
            else:
                prev_value = values[i-1]
                current_value = values[i]
                
                if prev_value != 0:
                    change = current_value - prev_value
                    percent = (change / prev_value) * 100
                    changes.append(round(change, 2))
                    change_percent.append(round(percent, 2))
                else:
                    changes.append(0.0)
                    change_percent.append(0.0)
        
        return changes, change_percent
    
    def get_index_data(self, symbols: List[str] = None, period: str = "7d") -> Dict[str, Any]:
        """
        インデックスデータを取得
        
        Args:
            symbols: 取得する銘柄リスト（None時は全銘柄）
            period: 期間（7d, 1m, 3m）
            
        Returns:
            インデックスデータの辞書
        """
        if symbols is None:
            symbols = list(self.INDEX_SYMBOLS.keys())
        
        logger.info(f"インデックスデータ取得開始: {symbols}, 期間: {period}")
        
        result = {
            "success": True,
            "data": {},
            "period": period,
            "lastUpdated": datetime.now().isoformat()
        }
        
        days = self.get_period_days(period)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days + 5)  # 余裕をもって取得
        
        for symbol in symbols:
            if symbol not in self.INDEX_SYMBOLS:
                logger.warning(f"未知のインデックス銘柄: {symbol}")
                continue
                
            try:
                logger.info(f"情報: {symbol} ({self.INDEX_SYMBOLS[symbol]['name']}) の実データを取得中...")
                
                # yfinanceでデータ取得
                ticker = yf.Ticker(symbol)
                hist = ticker.history(
                    start=start_date.strftime('%Y-%m-%d'),
                    end=end_date.strftime('%Y-%m-%d'),
                    interval='1d'
                )
                
                if hist.empty:
                    logger.error(f"エラー: {symbol}のデータが取得できませんでした")
                    # フォールバックデータ
                    result["data"][symbol] = self._get_fallback_data(symbol, days)
                    continue
                
                # 最新のN日分のデータを取得
                hist = hist.tail(days)
                
                # データ処理
                dates = [date.strftime('%Y-%m-%d') for date in hist.index]
                values = hist['Close'].round(2).tolist()
                
                # 前日比と騰落率を計算
                changes, change_percent = self.calculate_changes(values)
                
                result["data"][symbol] = {
                    "name": self.INDEX_SYMBOLS[symbol]["name"],
                    "symbol": symbol,
                    "dates": dates,
                    "values": values,
                    "changes": changes,
                    "changePercent": change_percent,
                    "description": self.INDEX_SYMBOLS[symbol]["description"]
                }
                
                logger.info(f"成功: {symbol}の実データを取得しました（{len(dates)}日分）")
                
            except Exception as e:
                logger.error(f"エラー: {symbol}のデータ取得でエラーが発生: {str(e)}")
                # エラー時はフォールバックデータを使用
                result["data"][symbol] = self._get_fallback_data(symbol, days)
        
        return result
    
    def get_single_index(self, symbol: str, period: str = "7d") -> Dict[str, Any]:
        """
        単一のインデックスデータを取得
        
        Args:
            symbol: 銘柄コード
            period: 期間
            
        Returns:
            単一インデックスデータ
        """
        data = self.get_index_data([symbol], period)
        
        if symbol in data["data"]:
            return {
                "success": True,
                "data": data["data"][symbol],
                "period": period,
                "lastUpdated": data["lastUpdated"]
            }
        else:
            return {
                "success": False,
                "error": f"インデックス銘柄 {symbol} が見つかりません",
                "data": None
            }
    
    def _get_fallback_data(self, symbol: str, days: int) -> Dict[str, Any]:
        """フォールバック用のモックデータを生成"""
        import random
        
        base_values = {
            "^N225": 28500,
            "^TPX": 1950,
            "2516.T": 850
        }
        
        base_value = base_values.get(symbol, 1000)
        dates = []
        values = []
        
        for i in range(days):
            date = datetime.now() - timedelta(days=days-1-i)
            dates.append(date.strftime('%Y-%m-%d'))
            
            # ランダムな変動を追加
            variation = random.uniform(-0.02, 0.02)  # ±2%の変動
            value = base_value * (1 + variation)
            values.append(round(value, 2))
        
        changes, change_percent = self.calculate_changes(values)
        
        return {
            "name": self.INDEX_SYMBOLS[symbol]["name"],
            "symbol": symbol,
            "dates": dates,
            "values": values,
            "changes": changes,
            "changePercent": change_percent,
            "description": self.INDEX_SYMBOLS[symbol]["description"],
            "note": "フォールバックデータ"
        }
    
    def get_available_indices(self) -> Dict[str, Any]:
        """利用可能なインデックス銘柄一覧を取得"""
        return {
            "success": True,
            "data": self.INDEX_SYMBOLS
        }

# グローバルインスタンス
index_service = IndexService()
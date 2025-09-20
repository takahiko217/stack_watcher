"""
シンプルな株価データ取得サービス
yfinanceライブラリを使用して日本株のデータを取得
"""

import yfinance as yf
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd


class StockService:
    """株価データ取得サービス"""
    
    def __init__(self):
        # 日本株の銘柄マッピング
        self.symbols_map = {
            "6326": {"code": "6326.T", "name": "クボタ"},
            "9984": {"code": "9984.T", "name": "ソフトバンクグループ"},
            "1377": {"code": "1377.T", "name": "サカタのタネ"}
        }
        
        # 期間のマッピング
        self.period_map = {
            "7d": "7d",
            "1m": "1mo", 
            "3m": "3mo"
        }
    
    def get_stock_data(self, symbol: str, period: str = "7d") -> Dict:
        """
        指定された銘柄の株価データを取得
        
        Args:
            symbol: 銘柄コード (例: "6326")
            period: 期間 ("7d", "1m", "3m")
            
        Returns:
            株価データの辞書
        """
        # 銘柄コードの検証
        if symbol not in self.symbols_map:
            raise ValueError(f"サポートされていない銘柄コード: {symbol}")
        
        # 期間の検証
        if period not in self.period_map:
            raise ValueError(f"サポートされていない期間: {period}")
        
        stock_info = self.symbols_map[symbol]
        yahoo_symbol = stock_info["code"]
        yf_period = self.period_map[period]
        
        try:
            # yfinanceでデータ取得
            print(f"情報: {symbol} ({yahoo_symbol}) の実データを取得中...")
            ticker = yf.Ticker(yahoo_symbol)
            data = ticker.history(period=yf_period)
            
            if data.empty:
                # データが取得できない場合はモックデータを返す
                print(f"警告: {symbol}の実データが取得できません。モックデータを返します。")
                return self._get_mock_data(symbol, stock_info["name"], period)
            
            # データを整形
            print(f"成功: {symbol}の実データを取得しました（{len(data)}日分）")
            formatted_data = self._format_stock_data(symbol, stock_info["name"], data)
            return formatted_data
            
        except Exception as e:
            print(f"エラー: {str(e)}。モックデータを返します。")
            return self._get_mock_data(symbol, stock_info["name"], period)
    
    def get_multiple_stocks(self, symbols: List[str], period: str = "7d") -> Dict:
        """
        複数銘柄の株価データを一括取得
        
        Args:
            symbols: 銘柄コードのリスト
            period: 期間
            
        Returns:
            複数銘柄の株価データ
        """
        stocks = []
        errors = []
        
        for symbol in symbols:
            try:
                stock_data = self.get_stock_data(symbol, period)
                stocks.append(stock_data)
            except Exception as e:
                errors.append({"symbol": symbol, "error": str(e)})
        
        return {
            "stocks": stocks,
            "errors": errors,
            "period": period,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_available_symbols(self) -> List[Dict]:
        """利用可能な銘柄一覧を取得"""
        symbols = []
        for code, info in self.symbols_map.items():
            symbols.append({
                "symbol": code,
                "name": info["name"],
                "market": "東証プライム"
            })
        return symbols
    
    def _format_stock_data(self, symbol: str, name: str, data: pd.DataFrame) -> Dict:
        """
        pandas DataFrameを辞書形式に変換
        
        Args:
            symbol: 銘柄コード
            name: 銘柄名
            data: pandas DataFrame
            
        Returns:
            整形された株価データ
        """
        data_points = []
        
        # インデックスを日付として扱う
        for date, row in data.iterrows():
            data_points.append({
                "date": date.isoformat(),
                "open": round(float(row["Open"]), 2),
                "high": round(float(row["High"]), 2),
                "low": round(float(row["Low"]), 2),
                "close": round(float(row["Close"]), 2),
                "volume": int(row["Volume"])
            })
        
        return {
            "symbol": symbol,
            "company_name": name,
            "data_points": data_points,
            "last_updated": datetime.now().isoformat()
        }
    
    def _get_mock_data(self, symbol: str, name: str, period: str) -> Dict:
        """
        現実的なモックデータを生成（実データが取得できない場合）
        
        Args:
            symbol: 銘柄コード
            name: 銘柄名  
            period: 期間
            
        Returns:
            モック株価データ
        """
        import random
        import math
        
        # 期間に応じてデータポイント数を決定
        period_days = {"7d": 7, "1m": 30, "3m": 90}
        days = period_days.get(period, 7)
        
        # 銘柄ごとの現実的なベース価格と特性
        stock_characteristics = {
            "6326": {
                "base_price": 2500, 
                "volatility": 0.03,  # 3%変動
                "trend": 0.002,      # 上昇トレンド
                "name": "クボタ"
            },
            "9984": {
                "base_price": 9000, 
                "volatility": 0.05,  # 5%変動（テック株らしく）
                "trend": -0.001,     # 微下降トレンド
                "name": "ソフトバンクグループ"
            },
            "1377": {
                "base_price": 4000, 
                "volatility": 0.04,  # 4%変動
                "trend": 0.001,      # 微上昇トレンド
                "name": "サカタのタネ"
            }
        }
        
        char = stock_characteristics.get(symbol, {
            "base_price": 1000, 
            "volatility": 0.03, 
            "trend": 0, 
            "name": name
        })
        
        data_points = []
        current_price = char["base_price"]
        
        # より現実的な価格変動の生成
        for i in range(days):
            # 日付を生成（今日から過去に遡る）
            date = datetime.now() - timedelta(days=days-i-1)
            
            # トレンドとランダム変動を組み合わせ
            trend_change = char["trend"] * current_price
            random_change = random.gauss(0, char["volatility"] * current_price)
            
            # 価格変動の計算
            price_change = trend_change + random_change
            
            # OHLC価格を現実的に生成
            open_price = current_price
            
            # High/Lowをより現実的に設定
            daily_range = abs(price_change) + random.uniform(0, char["volatility"] * current_price * 0.5)
            high_price = open_price + daily_range * random.uniform(0.3, 0.8)
            low_price = open_price - daily_range * random.uniform(0.3, 0.8)
            
            close_price = open_price + price_change
            
            # 価格が負になることを防ぐ
            close_price = max(close_price, char["base_price"] * 0.5)
            high_price = max(high_price, close_price)
            low_price = min(low_price, close_price)
            
            # 次の日の開始価格として更新
            current_price = close_price
            
            # ボリューム生成（曜日効果を考慮）
            base_volume = 1000000
            weekday = date.weekday()
            if weekday in [0, 4]:  # 月曜、金曜は取引が多い
                volume_multiplier = random.uniform(1.2, 1.8)
            elif weekday in [1, 2, 3]:  # 火水木は普通
                volume_multiplier = random.uniform(0.8, 1.3)
            else:  # 土日は除外されるが、念の為
                volume_multiplier = random.uniform(0.5, 0.8)
            
            volume = int(base_volume * volume_multiplier)
            
            data_points.append({
                "date": date.isoformat(),
                "open": round(open_price, 2),
                "high": round(high_price, 2), 
                "low": round(low_price, 2),
                "close": round(close_price, 2),
                "volume": volume
            })
        
        return {
            "symbol": symbol,
            "company_name": char["name"] + " (デモデータ)",
            "data_points": data_points,
            "last_updated": datetime.now().isoformat(),
            "is_mock": True,
            "note": "Yahoo Finance API制限のため、現実的なデモデータを表示しています"
        }


# グローバルインスタンス
stock_service = StockService()
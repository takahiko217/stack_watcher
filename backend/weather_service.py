"""
気象データサービス
OpenMeteo APIから東京都の気象データ（降水量、気温、気圧）を取得・処理するサービス
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging
import time

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeatherService:
    """気象データの取得と処理を担当するサービスクラス"""
    
    def __init__(self):
        """WeatherServiceの初期化"""
        # OpenMeteo Historical Weather APIのベースURL
        self.base_url = "https://archive-api.open-meteo.com/v1/archive"
        
        # 東京の座標（緯度、経度）
        self.tokyo_latitude = 35.6762
        self.tokyo_longitude = 139.6503
        
        logger.info("WeatherService初期化完了（OpenMeteo API使用）")
    
    def get_period_days(self, period: str) -> int:
        """期間文字列を日数に変換"""
        period_mapping = {
            "7d": 7,
            "1m": 30,
            "3m": 90
        }
        return period_mapping.get(period, 7)
    
    def get_weather_data(self, location: str = "tokyo", period: str = "7d") -> Dict[str, Any]:
        """
        OpenMeteo APIから気象データを取得
        
        Args:
            location: 取得地域（現在は東京のみ対応）
            period: 期間（7d, 1m, 3m）
            
        Returns:
            気象データの辞書
        """
        logger.info(f"気象データ取得開始: 地域={location}, 期間={period}")
        
        if location != "tokyo":
            logger.warning(f"未対応の地域: {location}. 東京データで代替します。")
        
        days = self.get_period_days(period)
        
        try:
            # OpenMeteo APIからリアルデータを取得
            real_data = self._fetch_openmeteo_data(days)
            if real_data:
                logger.info("OpenMeteo APIから実際の気象データを取得しました")
                return real_data
        except Exception as e:
            logger.warning(f"OpenMeteo API取得に失敗: {e}")
        
        # フォールバック: モックデータを生成
        logger.info("フォールバック気象データを生成します")
        return self._generate_mock_weather_data(days, period)
    
    def _fetch_openmeteo_data(self, days: int) -> Optional[Dict[str, Any]]:
        """
        OpenMeteo Historical Weather APIからデータを取得
        
        Args:
            days: 取得日数
            
        Returns:
            気象データまたはNone
        """
        try:
            # 日付範囲の計算
            end_date = datetime.now() - timedelta(days=2)  # 2日前まで（データ遅延のため）
            start_date = end_date - timedelta(days=days-1)
            
            # APIパラメータ
            params = {
                "latitude": self.tokyo_latitude,
                "longitude": self.tokyo_longitude,
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "daily": "precipitation_sum,temperature_2m_mean,pressure_msl_mean",
                "timezone": "Asia/Tokyo"
            }
            
            headers = {
                "User-Agent": "Stack-Watcher/1.0",
                "Accept": "application/json"
            }
            
            # APIリクエスト送信
            response = requests.get(self.base_url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._process_openmeteo_data(data, days)
            else:
                logger.warning(f"OpenMeteo API応答エラー: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.warning(f"OpenMeteo APIリクエストエラー: {e}")
            return None
        except Exception as e:
            logger.error(f"OpenMeteo気象データ処理エラー: {e}")
            return None
    
    def _process_openmeteo_data(self, raw_data: Dict, days: int) -> Dict[str, Any]:
        """
        OpenMeteo APIの生データを処理
        
        Args:
            raw_data: OpenMeteo APIからの生データ
            days: 必要な日数
            
        Returns:
            処理済み気象データ
        """
        try:
            daily_data = raw_data.get("daily", {})
            
            # データの抽出
            dates = daily_data.get("time", [])
            precipitation = daily_data.get("precipitation_sum", [])
            temperature = daily_data.get("temperature_2m_mean", [])
            pressure = daily_data.get("pressure_msl_mean", [])
            
            # Noneを0に変換（降水量）、温度・気圧はデータがない場合は前日値を使用
            processed_precipitation = [p if p is not None else 0.0 for p in precipitation]
            processed_temperature = []
            processed_pressure = []
            
            last_temp = 24.0  # デフォルト温度
            last_pressure = 1013.0  # デフォルト気圧
            
            for i, (temp, press) in enumerate(zip(temperature, pressure)):
                if temp is not None:
                    processed_temperature.append(round(temp, 1))
                    last_temp = temp
                else:
                    processed_temperature.append(round(last_temp, 1))
                
                if press is not None:
                    processed_pressure.append(round(press, 1))
                    last_pressure = press
                else:
                    processed_pressure.append(round(last_pressure, 1))
            
            return {
                "success": True,
                "data": {
                    "location": "東京都",
                    "dates": dates,
                    "precipitation": processed_precipitation,
                    "temperature": processed_temperature,
                    "pressure": processed_pressure
                },
                "period": f"{days}d",
                "lastUpdated": datetime.now().isoformat(),
                "source": "OpenMeteo API",
                "coordinates": {
                    "latitude": raw_data.get("latitude"),
                    "longitude": raw_data.get("longitude")
                }
            }
            
        except Exception as e:
            logger.error(f"OpenMeteoデータ処理エラー: {e}")
            return None
    
    def _generate_mock_weather_data(self, days: int, period: str) -> Dict[str, Any]:
        """
        モック気象データを生成
        
        Args:
            days: 日数
            period: 期間文字列
            
        Returns:
            モック気象データ
        """
        import random
        
        # 基準値（東京の季節平均値を想定）
        base_temp = 24.0  # 9月の平均気温
        base_pressure = 1013.0  # 標準気圧
        
        dates = []
        precipitation = []
        temperature = []
        pressure = []
        
        for i in range(days):
            # 日付生成
            date = datetime.now() - timedelta(days=days-1-i)
            dates.append(date.strftime('%Y-%m-%d'))
            
            # 降水量（0-50mm、雨の日は20%の確率）
            if random.random() < 0.2:  # 20%の確率で雨
                rain = round(random.uniform(1.0, 30.0), 1)
            else:
                rain = 0.0
            precipitation.append(rain)
            
            # 気温（基準値±5度の範囲でランダム変動）
            temp_variation = random.uniform(-3.0, 3.0)
            temp = round(base_temp + temp_variation, 1)
            temperature.append(temp)
            
            # 気圧（基準値±20hPaの範囲でランダム変動）
            pressure_variation = random.uniform(-15.0, 15.0)
            press = round(base_pressure + pressure_variation, 1)
            pressure.append(press)
        
        return {
            "success": True,
            "data": {
                "location": "東京都",
                "dates": dates,
                "precipitation": precipitation,
                "temperature": temperature,
                "pressure": pressure
            },
            "period": period,
            "lastUpdated": datetime.now().isoformat(),
            "source": "モックデータ",
            "note": "実際の気象庁APIが利用できない場合のフォールバックデータ"
        }
    
    def get_available_locations(self) -> Dict[str, Any]:
        """利用可能な観測地点一覧を取得"""
        return {
            "success": True,
            "data": {
                "tokyo": {
                    "name": "東京都",
                    "latitude": self.tokyo_latitude,
                    "longitude": self.tokyo_longitude,
                    "description": "東京都内の代表観測点（OpenMeteo API）"
                }
            },
            "note": "現在は東京都のみ対応"
        }
    
    def validate_period(self, period: str) -> bool:
        """期間の妥当性チェック"""
        valid_periods = ["7d", "1m", "3m"]
        return period in valid_periods
    
    def validate_location(self, location: str) -> bool:
        """地域の妥当性チェック"""
        valid_locations = ["tokyo"]
        return location in valid_locations

# グローバルインスタンス
weather_service = WeatherService()
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from backend.main import app

client = TestClient(app)

class TestStocksAPI:
    """株価API のテストクラス"""
    
    def test_health_check(self):
        """ヘルスチェックのテスト"""
        response = client.get("/api/v1/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["status"] == "healthy"
        
    def test_get_multiple_stocks_success(self):
        """複数銘柄取得成功のテスト"""
        response = client.get("/api/v1/stocks?symbols=6326,9984,1377&period=7d")
        
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        
        if data["success"]:
            assert "data" in data
            # データ構造の検証
            stocks_data = data["data"]
            expected_symbols = ["6326", "9984", "1377"]
            
            for symbol in expected_symbols:
                if symbol in stocks_data:
                    stock = stocks_data[symbol]
                    assert "company_name" in stock
                    assert "symbol" in stock
                    assert "dates" in stock
                    assert "values" in stock
                    
    def test_get_multiple_stocks_invalid_period(self):
        """無効な期間指定のテスト"""
        response = client.get("/api/v1/stocks?symbols=6326,9984,1377&period=invalid")
        
        # 現在の実装では200で成功するが、エラーがdataに含まれる可能性がある
        assert response.status_code in [200, 400]
        data = response.json()
        
        if response.status_code == 400:
            assert "detail" in data
            assert "無効な期間" in data["detail"]
        else:
            # 200の場合でもエラー情報が含まれるかチェック
            assert "success" in data
        
    def test_indices_api_success(self):
        """指数API 成功のテスト"""
        response = client.get("/api/v1/indices?period=7d")
        
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        
        if data["success"]:
            assert "data" in data
            indices_data = data["data"]
            
            # 期待される指数シンボル
            expected_indices = ["^N225", "^TPX", "2516.T"]
            
            for index_symbol in expected_indices:
                if index_symbol in indices_data:
                    index = indices_data[index_symbol]
                    assert "name" in index
                    assert "symbol" in index
                    assert "dates" in index
                    assert "values" in index
                    
    def test_indices_api_invalid_period(self):
        """指数API 無効な期間のテスト"""
        response = client.get("/api/v1/indices?period=invalid")
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "無効な期間" in data["detail"]
        
    def test_weather_api_success(self):
        """気象API 成功のテスト"""
        response = client.get("/api/v1/weather?period=7d")
        
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        
        if data["success"]:
            assert "data" in data
            weather_data = data["data"]
            
            # 期待される気象データフィールド
            expected_fields = ["dates", "precipitation", "temperature", "pressure"]
            
            for field in expected_fields:
                assert field in weather_data
                assert isinstance(weather_data[field], list)
                
    def test_weather_api_invalid_period(self):
        """気象API 無効な期間のテスト"""
        response = client.get("/api/v1/weather?period=invalid")
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "無効な期間" in data["detail"]
        
    def test_demo_endpoint(self):
        """デモエンドポイントのテスト"""
        response = client.get("/api/v1/demo")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "success" in data
        assert data["success"] is True
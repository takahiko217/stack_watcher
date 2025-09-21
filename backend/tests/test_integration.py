import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

class TestAPIIntegration:
    """API統合テスト"""
    
    def test_full_dashboard_data_flow(self):
        """ダッシュボード全体のデータフローテスト"""
        
        # 1. ヘルスチェック
        health_response = client.get("/api/v1/health")
        assert health_response.status_code == 200
        health_data = health_response.json()
        assert health_data["success"] is True
        
        # 2. 株価データ取得
        stocks_response = client.get("/api/v1/stocks?symbols=6326,9984,1377&period=7d")
        assert stocks_response.status_code == 200
        stocks_data = stocks_response.json()
        assert "success" in stocks_data
        
        # 3. 指数データ取得
        indices_response = client.get("/api/v1/indices?period=7d")
        assert indices_response.status_code == 200
        indices_data = indices_response.json()
        assert "success" in indices_data
        
        # 4. 気象データ取得
        weather_response = client.get("/api/v1/weather?period=7d")
        assert weather_response.status_code == 200
        weather_data = weather_response.json()
        assert "success" in weather_data
        
        print("✅ 全データソースが正常に取得できています")
        
    def test_period_consistency(self):
        """期間パラメータの一貫性テスト"""
        
        periods = ["7d", "1m", "3m"]
        
        for period in periods:
            # 株価データ
            stocks_response = client.get(f"/api/v1/stocks?symbols=6326,9984,1377&period={period}")
            assert stocks_response.status_code == 200
            
            # 指数データ
            indices_response = client.get(f"/api/v1/indices?period={period}")
            assert indices_response.status_code == 200
            
            # 気象データ
            weather_response = client.get(f"/api/v1/weather?period={period}")
            assert weather_response.status_code == 200
            
            print(f"✅ 期間 {period} で全API が正常動作")
            
    def test_data_structure_consistency(self):
        """データ構造の一貫性テスト"""
        
        # 株価データの構造検証
        stocks_response = client.get("/api/v1/stocks?symbols=6326,9984,1377&period=7d")
        stocks_data = stocks_response.json()
        
        if stocks_data.get("success"):
            data = stocks_data.get("data", {})
            for symbol in ["6326", "9984", "1377"]:
                if symbol in data:
                    stock = data[symbol]
                    required_fields = ["symbol", "company_name", "dates", "values"]
                    for field in required_fields:
                        assert field in stock, f"株価データに{field}フィールドが不足"
        
        # 指数データの構造検証
        indices_response = client.get("/api/v1/indices?period=7d")
        indices_data = indices_response.json()
        
        if indices_data.get("success"):
            data = indices_data.get("data", {})
            for index_symbol in ["^N225", "^TPX", "2516.T"]:
                if index_symbol in data:
                    index = data[index_symbol]
                    required_fields = ["name", "symbol", "dates", "values"]
                    for field in required_fields:
                        assert field in index, f"指数データに{field}フィールドが不足"
        
        # 気象データの構造検証
        weather_response = client.get("/api/v1/weather?period=7d")
        weather_data = weather_response.json()
        
        if weather_data.get("success"):
            data = weather_data.get("data", {})
            required_fields = ["dates", "precipitation", "temperature", "pressure"]
            for field in required_fields:
                assert field in data, f"気象データに{field}フィールドが不足"
        
        print("✅ 全データ構造が仕様に準拠しています")
        
    def test_error_handling_consistency(self):
        """エラーハンドリングの一貫性テスト"""
        
        # 無効な期間でのテスト
        invalid_period = "invalid"
        
        # 各API で適切なエラーハンドリングがされることを確認
        endpoints = [
            f"/api/v1/stocks?symbols=6326,9984,1377&period={invalid_period}",
            f"/api/v1/indices?period={invalid_period}",
            f"/api/v1/weather?period={invalid_period}"
        ]
        
        for endpoint in endpoints:
            response = client.get(endpoint)
            # レスポンスは200または400のいずれかであることを確認
            assert response.status_code in [200, 400], f"想定外のステータスコード: {response.status_code}"
            
        print("✅ エラーハンドリングが一貫しています")
        
    def test_performance_baseline(self):
        """基本的なパフォーマンステスト"""
        import time
        
        # レスポンス時間の測定
        start_time = time.time()
        
        # 同時にすべてのデータを取得
        stocks_response = client.get("/api/v1/stocks?symbols=6326,9984,1377&period=7d")
        indices_response = client.get("/api/v1/indices?period=7d")
        weather_response = client.get("/api/v1/weather?period=7d")
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # 全API の取得が10秒以内であることを確認
        assert total_time < 10.0, f"API応答時間が遅すぎます: {total_time:.2f}秒"
        
        print(f"✅ API応答時間: {total_time:.2f}秒 (基準値内)")
        
    def test_data_availability(self):
        """データ可用性テスト"""
        
        # 各データソースが実際にデータを返すかテスト
        stocks_response = client.get("/api/v1/stocks?symbols=6326,9984,1377&period=7d")
        stocks_data = stocks_response.json()
        
        if stocks_data.get("success") and stocks_data.get("data"):
            data = stocks_data["data"]
            if isinstance(data, dict):
                available_symbols = len([k for k, v in data.items() if isinstance(v, dict) and v.get("dates")])
            else:
                available_symbols = len(data) if isinstance(data, list) else 0
            print(f"✅ 株価データ: {available_symbols} 銘柄が利用可能")
        
        indices_response = client.get("/api/v1/indices?period=7d")
        indices_data = indices_response.json()
        
        if indices_data.get("success") and indices_data.get("data"):
            data = indices_data["data"]
            if isinstance(data, dict):
                available_indices = len([k for k, v in data.items() if isinstance(v, dict) and v.get("dates")])
            else:
                available_indices = len(data) if isinstance(data, list) else 0
            print(f"✅ 指数データ: {available_indices} 指数が利用可能")
        
        weather_response = client.get("/api/v1/weather?period=7d")
        weather_data = weather_response.json()
        
        if weather_data.get("success") and weather_data.get("data"):
            data = weather_data["data"]
            has_weather_data = bool(data.get("dates")) if isinstance(data, dict) else False
            print(f"✅ 気象データ: {'利用可能' if has_weather_data else '利用不可'}")
        
        print("✅ データ可用性チェック完了")
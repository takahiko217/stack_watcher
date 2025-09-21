import pytest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, timezone
import sys
import os

# バックエンドモジュールへのパスを追加
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from backend.services.stock_service import StockService
except ImportError:
    # stock_serviceが存在しない場合はスキップ
    pytest.skip("stock_service module not found", allow_module_level=True)

class TestStockService:
    """StockService のテストクラス"""
    
    @pytest.fixture
    def stock_service(self):
        return StockService()
    
    def test_validate_symbol_valid(self, stock_service):
        """有効な銘柄コードのバリデーション"""
        valid_symbols = ["6326", "9984", "1377"]
        
        for symbol in valid_symbols:
            assert stock_service.validate_symbol(symbol) is True
            
    def test_validate_symbol_invalid(self, stock_service):
        """無効な銘柄コードのバリデーション"""
        invalid_symbols = ["9999", "invalid", "", None]
        
        for symbol in invalid_symbols:
            assert stock_service.validate_symbol(symbol) is False
            
    def test_validate_period_valid(self, stock_service):
        """有効な期間のバリデーション"""
        valid_periods = ["7d", "1m", "3m"]
        
        for period in valid_periods:
            assert stock_service.validate_period(period) is True
            
    def test_validate_period_invalid(self, stock_service):
        """無効な期間のバリデーション"""
        invalid_periods = ["1d", "6m", "1y", "invalid", "", None]
        
        for period in invalid_periods:
            assert stock_service.validate_period(period) is False
"""
アプリケーション設定ファイル

環境変数や設定値を管理するためのモジュールです。
初心者向けに各設定の説明を含めています。
"""

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """
    アプリケーション設定クラス
    
    環境変数から設定値を読み込みます。
    .envファイルを使用して設定を管理することも可能です。
    """
    
    # アプリケーション基本設定
    app_name: str = "Stack Watcher"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # データベース設定
    database_url: str = "sqlite:///./stack_watcher.db"
    
    # セキュリティ設定
    secret_key: str = "your-secret-key-here"  # 本番環境では必ず変更してください
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS設定
    allowed_origins: list = ["http://localhost:3000"]
    
    # ログ設定
    log_level: str = "INFO"
    
    class Config:
        """
        設定クラスの設定
        
        .envファイルから環境変数を読み込む設定
        """
        env_file = ".env"
        case_sensitive = False

# 設定インスタンスを作成
# アプリケーション全体でこのインスタンスを使用します
settings = Settings()
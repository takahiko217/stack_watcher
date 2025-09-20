# Stack Watcher API設計書

## 1. API概要

### 1.1 基本情報
- **API名**: Stack Watcher REST API
- **バージョン**: v1.0
- **ベースURL**: `http://localhost:8000/api/v1`
- **認証方式**: JWT Bearer Token（Phase 2以降）
- **データ形式**: JSON
- **文字エンコーディング**: UTF-8

### 1.2 設計原則
- RESTful API設計
- 一貫性のあるレスポンス形式
- 適切なHTTPステータスコード使用
- エラーハンドリングの統一

## 2. 共通仕様

### 2.1 共通レスポンス形式

#### 成功レスポンス
```json
{
  "success": true,
  "data": {
    // 実際のデータ
  },
  "message": "成功メッセージ",
  "timestamp": "2025-09-20T10:30:00Z"
}
```

#### エラーレスポンス
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "エラーメッセージ",
    "details": "詳細なエラー情報（開発時のみ）"
  },
  "timestamp": "2025-09-20T10:30:00Z"
}
```

### 2.2 共通パラメータ

#### 期間指定
- `period`: `7d` | `1m` | `3m`
  - `7d`: 7日間
  - `1m`: 1ヶ月（30日）
  - `3m`: 3ヶ月（90日）

#### 日付形式
- ISO 8601形式: `YYYY-MM-DDTHH:mm:ssZ`
- 例: `2025-09-20T09:00:00Z`

### 2.3 HTTPステータスコード
- `200`: 成功
- `400`: リクエストエラー
- `401`: 認証エラー
- `403`: 権限エラー
- `404`: リソースが見つからない
- `429`: レート制限
- `500`: サーバーエラー
- `503`: サービス利用不可

## 3. 株価データAPI

### 3.1 株価データ取得

#### エンドポイント
```
GET /api/v1/stocks/{symbol}
```

#### パラメータ
- **パス**: 
  - `symbol` (string, required): 銘柄コード
    - `6326`: クボタ
    - `9984`: ソフトバンク
    - `1377`: サカタのタネ

- **クエリ**:
  - `period` (string, optional): 期間 (default: `7d`)
  - `start_date` (string, optional): 開始日 (ISO 8601)
  - `end_date` (string, optional): 終了日 (ISO 8601)

#### レスポンス例
```json
{
  "success": true,
  "data": {
    "symbol": "6326",
    "company_name": "クボタ",
    "period": "7d",
    "data_points": [
      {
        "date": "2025-09-20T09:00:00Z",
        "open": 2500.0,
        "high": 2550.0,
        "low": 2480.0,
        "close": 2530.0,
        "volume": 1000000,
        "adj_close": 2530.0
      }
    ],
    "last_updated": "2025-09-20T15:00:00Z"
  },
  "message": "株価データを取得しました",
  "timestamp": "2025-09-20T15:00:15Z"
}
```

### 3.2 複数銘柄の株価データ取得

#### エンドポイント
```
GET /api/v1/stocks
```

#### パラメータ
- **クエリ**:
  - `symbols` (string, required): カンマ区切りの銘柄コード
  - `period` (string, optional): 期間 (default: `7d`)

#### レスポンス例
```json
{
  "success": true,
  "data": {
    "period": "7d",
    "stocks": [
      {
        "symbol": "6326",
        "company_name": "クボタ",
        "data_points": [...]
      },
      {
        "symbol": "9984", 
        "company_name": "ソフトバンク",
        "data_points": [...]
      }
    ],
    "last_updated": "2025-09-20T15:00:00Z"
  }
}
```

## 4. 銘柄マスタAPI

### 4.1 銘柄一覧取得

#### エンドポイント
```
GET /api/v1/stocks/symbols
```

#### レスポンス例
```json
{
  "success": true,
  "data": {
    "symbols": [
      {
        "symbol": "6326",
        "company_name": "クボタ",
        "market": "東証プライム",
        "sector": "機械",
        "industry": "農業用機械"
      },
      {
        "symbol": "9984",
        "company_name": "ソフトバンクグループ",
        "market": "東証プライム", 
        "sector": "情報・通信業",
        "industry": "その他の情報・通信業"
      },
      {
        "symbol": "1377",
        "company_name": "サカタのタネ",
        "market": "東証プライム",
        "sector": "水産・農林業",
        "industry": "農業"
      }
    ]
  }
}
```

## 5. カラーマスタAPI

### 5.1 カラー設定取得

#### エンドポイント
```
GET /api/v1/colors/master
```

#### レスポンス例
```json
{
  "success": true,
  "data": {
    "colors": {
      "stocks": {
        "6326": "#2563eb",
        "9984": "#dc2626", 
        "1377": "#059669"
      },
      "indices": {
        "nikkei225": "#7c3aed",
        "topix": "#ea580c"
      },
      "system": {
        "primary": "#1e40af",
        "success": "#059669",
        "warning": "#ea580c",
        "error": "#dc2626",
        "background": "#f8fafc",
        "surface": "#ffffff",
        "text_primary": "#1f2937",
        "text_secondary": "#6b7280",
        "border": "#e5e7eb"
      }
    }
  }
}
```

## 6. ヘルスチェックAPI

### 6.1 システムステータス

#### エンドポイント
```
GET /api/v1/health
```

#### レスポンス例
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "version": "1.0.0",
    "uptime": "24h 15m 30s",
    "database": {
      "status": "connected",
      "response_time": "5ms"
    },
    "external_apis": {
      "yahoo_finance": {
        "status": "available",
        "last_check": "2025-09-20T15:00:00Z"
      }
    }
  }
}
```

## 7. エラーハンドリング

### 7.1 エラーコード一覧

| コード | メッセージ | 説明 |
|--------|------------|------|
| `INVALID_SYMBOL` | 無効な銘柄コードです | 存在しない銘柄コード |
| `INVALID_PERIOD` | 無効な期間指定です | サポートされていない期間 |
| `INVALID_DATE_RANGE` | 無効な日付範囲です | 開始日が終了日より後など |
| `DATA_NOT_FOUND` | データが見つかりません | 指定期間のデータが存在しない |
| `EXTERNAL_API_ERROR` | 外部APIエラー | Yahoo Finance APIエラー |
| `RATE_LIMIT_EXCEEDED` | レート制限に達しました | API呼び出し制限 |
| `INTERNAL_SERVER_ERROR` | サーバー内部エラー | 予期しないエラー |

### 7.2 エラーレスポンス例

#### 無効な銘柄コード
```json
{
  "success": false,
  "error": {
    "code": "INVALID_SYMBOL",
    "message": "銘柄コード '9999' は存在しません",
    "details": "サポートされている銘柄コード: 6326, 9984, 1377"
  },
  "timestamp": "2025-09-20T15:00:15Z"
}
```

#### レート制限
```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "API呼び出し制限に達しました",
    "details": "1分後に再試行してください"
  },
  "timestamp": "2025-09-20T15:00:15Z"
}
```

## 8. レート制限

### 8.1 制限値
- **一般ユーザー**: 100リクエスト/分
- **開発者モード**: 1000リクエスト/分

### 8.2 レスポンスヘッダー
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642780800
```

## 9. キャッシュ戦略

### 9.1 キャッシュ期間
- **株価データ**: 15分
- **銘柄マスタ**: 24時間
- **カラーマスタ**: 24時間

### 9.2 キャッシュヘッダー
```
Cache-Control: public, max-age=900
ETag: "abc123"
Last-Modified: Wed, 20 Sep 2025 15:00:00 GMT
```

## 10. APIバージョニング

### 10.1 バージョン管理方式
- URL パス方式: `/api/v1/`
- 後方互換性の維持
- 廃止予定APIの事前通知

### 10.2 バージョン履歴
- `v1.0`: 初回リリース（Phase 1 MVP）

---

**作成日**: 2025年9月20日  
**バージョン**: 1.0  
**対象フェーズ**: Phase 1 MVP
# API仕様書

## 文書情報

| 項目 | 値 |
|------|-----|
| 文書タイトル | [プロジェクト名] API仕様書 |
| バージョン | 1.0.0 |
| 作成日 | YYYY-MM-DD |
| 最終更新日 | YYYY-MM-DD |
| 作成者 | [作成者名] |
| 承認者 | [承認者名] |

## 目次
1. [概要](#概要)
2. [認証](#認証)
3. [エンドポイント](#エンドポイント)
4. [データ型](#データ型)
5. [エラーハンドリング](#エラーハンドリング)
6. [レート制限](#レート制限)
7. [変更履歴](#変更履歴)

## 概要

### API の目的
このAPIの目的と提供する機能について説明してください。

### ベースURL
```
https://api.example.com/v1
```

### プロトコル
- プロトコル: HTTPS
- データ形式: JSON
- 文字エンコーディング: UTF-8

### バージョニング
APIのバージョニング戦略について説明してください。

## 認証

### 認証方式
使用する認証方式について説明してください。

#### API キー認証の例
```http
Authorization: Bearer your-api-key
```

#### OAuth 2.0 の例
```http
Authorization: Bearer your-access-token
```

### 認証エラー
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "認証が必要です"
  }
}
```

## エンドポイント

### エンドポイント一覧

| エンドポイント | メソッド | 説明 | 認証 |
|---------------|----------|------|------|
| `/health` | GET | ヘルスチェック | 不要 |
| `/users` | GET | ユーザー一覧取得 | 必要 |
| `/users` | POST | ユーザー作成 | 必要 |
| `/users/{id}` | GET | ユーザー詳細取得 | 必要 |
| `/users/{id}` | PUT | ユーザー更新 | 必要 |
| `/users/{id}` | DELETE | ユーザー削除 | 必要 |

### エンドポイント詳細

#### GET /health
システムの状態を確認します。

**リクエスト**
- パラメータ: なし
- 認証: 不要

**レスポンス**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "version": "1.0.0"
}
```

**ステータスコード**
- `200 OK`: 正常
- `503 Service Unavailable`: サービス利用不可

#### GET /users
ユーザー一覧を取得します。

**リクエスト**
- 認証: 必要
- パラメータ:

| パラメータ | 型 | 必須 | 説明 | デフォルト |
|-----------|----|----|------|-----------|
| page | integer | No | ページ番号 | 1 |
| limit | integer | No | 取得件数 | 20 |
| sort | string | No | ソート順 | created_at |

**リクエスト例**
```http
GET /users?page=1&limit=10&sort=name
Authorization: Bearer your-api-key
```

**レスポンス**
```json
{
  "data": [
    {
      "id": 1,
      "name": "田中太郎",
      "email": "tanaka@example.com",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 100,
    "total_pages": 10
  }
}
```

**ステータスコード**
- `200 OK`: 正常
- `401 Unauthorized`: 認証エラー
- `403 Forbidden`: 権限不足

#### POST /users
新しいユーザーを作成します。

**リクエスト**
- 認証: 必要
- Content-Type: application/json

**リクエストボディ**
```json
{
  "name": "田中太郎",
  "email": "tanaka@example.com",
  "password": "secure_password"
}
```

**レスポンス**
```json
{
  "id": 1,
  "name": "田中太郎",
  "email": "tanaka@example.com",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

**ステータスコード**
- `201 Created`: 作成成功
- `400 Bad Request`: 入力値エラー
- `401 Unauthorized`: 認証エラー
- `409 Conflict`: 重複エラー

#### GET /users/{id}
指定されたIDのユーザー詳細を取得します。

**リクエスト**
- 認証: 必要
- パスパラメータ:

| パラメータ | 型 | 必須 | 説明 |
|-----------|----|----|------|
| id | integer | Yes | ユーザーID |

**レスポンス**
```json
{
  "id": 1,
  "name": "田中太郎",
  "email": "tanaka@example.com",
  "profile": {
    "bio": "自己紹介",
    "avatar_url": "https://example.com/avatar.jpg"
  },
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

**ステータスコード**
- `200 OK`: 正常
- `401 Unauthorized`: 認証エラー
- `404 Not Found`: ユーザーが存在しない

## データ型

### 共通データ型

#### User
ユーザー情報を表すオブジェクト

| フィールド | 型 | 必須 | 説明 |
|-----------|----|----|------|
| id | integer | Yes | ユーザーID |
| name | string | Yes | ユーザー名 |
| email | string | Yes | メールアドレス |
| created_at | string (ISO 8601) | Yes | 作成日時 |
| updated_at | string (ISO 8601) | Yes | 更新日時 |

#### Pagination
ページネーション情報

| フィールド | 型 | 必須 | 説明 |
|-----------|----|----|------|
| page | integer | Yes | 現在のページ |
| limit | integer | Yes | 1ページあたりの件数 |
| total | integer | Yes | 総件数 |
| total_pages | integer | Yes | 総ページ数 |

## エラーハンドリング

### エラーレスポンス形式
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "エラーメッセージ",
    "details": "詳細情報（オプション）"
  }
}
```

### エラーコード一覧

| ステータスコード | エラーコード | 説明 |
|-----------------|-------------|------|
| 400 | BAD_REQUEST | リクエストが不正 |
| 401 | UNAUTHORIZED | 認証が必要 |
| 403 | FORBIDDEN | 権限不足 |
| 404 | NOT_FOUND | リソースが存在しない |
| 409 | CONFLICT | データの競合 |
| 422 | VALIDATION_ERROR | バリデーションエラー |
| 429 | RATE_LIMIT_EXCEEDED | レート制限に達した |
| 500 | INTERNAL_ERROR | サーバー内部エラー |

### バリデーションエラーの例
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "入力値にエラーがあります",
    "details": {
      "email": ["有効なメールアドレスを入力してください"],
      "password": ["パスワードは8文字以上である必要があります"]
    }
  }
}
```

## レート制限

### 制限値
- 認証済みユーザー: 1000リクエスト/時間
- 未認証ユーザー: 100リクエスト/時間

### レスポンスヘッダー
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

### レート制限に達した場合
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "レート制限に達しました。しばらく時間をおいてから再試行してください。"
  }
}
```

## 変更履歴

### バージョン 1.0.0 (YYYY-MM-DD)
- 初版作成

---

**注意**: このAPI仕様書は国際標準（OpenAPI Specification、RFC等）に基づいて作成されています。実装に応じて適切に更新してください。
# Stack Watcher - Vue.js + FastAPI アプリケーション

Databricks Apps プラットフォーム向けのフルスタックアプリケーションです。Vue.js フロントエンドと FastAPI バックエンドを組み合わせ、技術スタック監視システムを提供します。

## アーキテクチャ

```
Vue.js Frontend (TypeScript + Vite)
    ↓ API calls
FastAPI Backend (Python)
    ↓ Serves static files + API
Databricks Apps
```

## Databricks Apps 開発ワークフロー

### 基本概念

Databricks Apps は、バックエンドサーバーがフロントエンドの静的ファイルを配信する構成になっています。そのため：

- **バックエンドのみ Databricks にデプロイ**：`app.yaml` で uvicorn サーバーを起動
- **フロントエンドは静的ファイル**：ビルドされた dist ファイルを backend/static に配置
- **ローカル開発**：VSCode でコード編集し、完了後に Databricks Workspace と同期

### 1. 初期セットアップ

```bash
# Python 仮想環境作成
python3 -m venv venv
source venv/bin/activate

# Python 依存関係インストール
pip install -r requirements.txt

# Node.js 依存関係インストール（フロントエンド用）
npm install
```

### 2. ローカル開発

#### 開発サーバー起動

```bash
# バックエンド起動 (ターミナル1)
source venv/bin/activate
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8003

# フロントエンド開発サーバー起動 (ターミナル2) - オプション
cd frontend
npm run dev --host 0.0.0.0 --port 5173
```

- フロントエンド: http://localhost:5173 (開発用・ホットリロード対応)
- バックエンド API: http://localhost:8003/docs (Swagger UI)
- 統合アプリ: http://localhost:8003 (本番相当)

#### フロントエンド更新時

```bash
# フロントエンドをビルドして backend/static に出力
npm run build
```

**重要**: `vite.config.js` で `outDir: '../backend/static'` に設定済みのため、ビルド時に自動的にバックエンドの静的ファイルディレクトリに配置されます。

### 3. Databricks Workspace との同期

#### ファイル同期 (初回)

```bash
# Workspace からローカルにテンプレートをダウンロード（初回のみ）
databricks workspace export-dir /Workspace/Users/[your-email]/databricks_apps/[app-name] .

# ローカルからWorkspaceへリアルタイム同期開始
databricks sync --watch . /Workspace/Users/[your-email]/databricks_apps/[app-name]
```

#### 継続的な同期

`databricks sync --watch` コマンドを実行中は、ローカルファイルの変更が自動的に Databricks Workspace に同期されます。

### 4. Databricks Apps デプロイ

```bash
# アプリを Databricks Apps にデプロイ
databricks apps deploy [app-name] --source-code-path /Workspace/Users/[your-email]/databricks_apps/[app-name]
```

### 5. プロジェクト構成

```
stack_watcher/
├── app.yaml                    # Databricks Apps 設定ファイル
├── requirements.txt            # Python 依存関係
├── backend/
│   ├── main.py                # FastAPI アプリケーション
│   ├── static/                # フロントエンドビルド出力先
│   └── app/
│       └── core/
│           └── config.py      # 設定管理
├── frontend/
│   ├── index.html
│   ├── vite.config.js         # Vite 設定（ビルド出力先設定含む）
│   └── src/
│       ├── main.js           # Vue.js エントリーポイント
│       └── App.vue           # メインコンポーネント
└── docs/                      # ドキュメント
```

### 6. 重要なファイル

#### `app.yaml`
```yaml
command: ["uvicorn", "backend.main:app"]
```
Databricks Apps でのアプリケーション起動コマンドを定義。

#### `backend/main.py`
- FastAPI アプリケーション
- `/api/*` ルートでバックエンド API を提供
- `/` で静的ファイル（フロントエンド）を配信
- SPA ルーティング対応のフォールバック機能

#### `frontend/vite.config.js`
```javascript
export default defineConfig({
  plugins: [vue()],
  build: {
    outDir: resolve(__dirname, '../backend/static'),
    emptyOutDir: true,
  }
})
```
フロントエンドビルド時に `backend/static` に出力するよう設定。

### 7. 開発のベストプラクティス

1. **フロントエンド変更時**：
   - 開発中は `npm run dev` でホットリロードを活用
   - 完了したら `npm run build` でビルドし、`backend/static` を更新

2. **バックエンド変更時**：
   - `uvicorn --reload` でサーバー自動再起動を活用
   - API 変更時はフロントエンド側の型定義も更新

3. **同期とデプロイ**：
   - `databricks sync --watch` を常時実行
   - 重要な変更後は `databricks apps deploy` でデプロイテスト

4. **トラブルシューティング**：
   - フロントエンドが表示されない → `npm run build` 実行確認
   - API が応答しない → バックエンドのログとCORS設定確認
   - Databricks 同期エラー → 認証とパス設定確認

## API エンドポイント

- `GET /api/hello` - Hello world メッセージ
- `GET /api/health` - ヘルスチェック
- `GET /health` - システムヘルスチェック
- `GET /api/data` - サンプルデータ（チャート用）
- `GET /docs` - FastAPI 自動生成ドキュメント

## トラブルシューティング

### よくある問題

1. **フロントエンドが表示されない**
   ```bash
   npm run build  # backend/static を更新
   ```

2. **API 接続エラー**
   - CORS 設定確認: `backend/app/core/config.py`
   - プロキシ設定確認: `frontend/vite.config.js`

3. **Databricks 同期エラー**
   ```bash
   databricks auth login  # 認証確認
   ```

## 参考資料

- [Databricks Apps 公式ドキュメント](https://docs.databricks.com/en/dev-tools/databricks-apps.html)
- [FastAPI 公式ドキュメント](https://fastapi.tiangolo.com/)
- [Vue.js 公式ガイド](https://vuejs.org/guide/)
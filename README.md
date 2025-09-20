# Stack Watcher

## 📋 概要

Stack Watcher は、Vue.js と FastAPI を使用して構築された現代的なWebアプリケーションです。初心者でも理解しやすい構造と豊富なコメントで、学習と実用の両方に適した設計になっています。

## 🎯 特徴

- **🔰 初心者フレンドリー**: 豊富なコメントと分かりやすいコード構造
- **🏗️ モジュラー設計**: 機能ごとに分離された保守しやすい構造
- **⚡ 最新技術**: Vue.js 3 + FastAPI の組み合わせ
- **📚 国際標準対応**: ドキュメント管理において国際標準に準拠
- **🚀 高性能**: 最適化されたビルドとデプロイメント

## 🛠️ 使用技術

### フロントエンド
- **Vue.js 3** - プログレッシブフレームワーク
- **Vue Router** - シングルページアプリケーション
- **Pinia** - 状態管理
- **Vite** - 高速ビルドツール
- **Axios** - HTTP クライアント

### バックエンド
- **FastAPI** - 高性能Webフレームワーク
- **Python 3.11+** - プログラミング言語
- **Uvicorn** - ASGIサーバー
- **SQLAlchemy** - ORMライブラリ
- **Pydantic** - データバリデーション

## 📁 プロジェクト構造

```
stack_watcher/
├── frontend/                 # Vue.js フロントエンド
│   ├── src/
│   │   ├── components/       # 再利用可能なコンポーネント
│   │   ├── views/           # ページコンポーネント
│   │   ├── stores/          # Pinia状態管理
│   │   ├── assets/          # 静的アセット
│   │   ├── utils/           # ユーティリティ関数
│   │   ├── router.js        # ルーティング設定
│   │   ├── App.vue          # ルートコンポーネント
│   │   └── main.js          # エントリーポイント
│   ├── public/              # 公開ファイル
│   ├── package.json         # 依存関係管理
│   ├── vite.config.js       # Vite設定
│   └── index.html           # HTMLテンプレート
├── backend/                 # FastAPI バックエンド
│   ├── app/
│   │   ├── api/             # APIエンドポイント
│   │   ├── models/          # データモデル
│   │   ├── core/            # コア機能（設定など）
│   │   └── utils/           # ユーティリティ関数
│   ├── main.py              # FastAPIアプリケーション
│   └── requirements.txt     # Python依存関係
├── scripts/                 # 環境設定・起動スクリプト
│   ├── setup.sh             # 環境セットアップ
│   └── start.sh             # アプリケーション起動
├── docs/                    # ドキュメント
│   ├── templates/           # ドキュメントテンプレート
│   ├── api/                 # API仕様書
│   └── user_manual/         # ユーザーマニュアル
├── config/                  # 設定ファイル
├── README.md                # このファイル
└── .gitignore               # Git除外設定
```

### 📂 フォルダ構造の説明

#### フロントエンド (`frontend/`)
- **`src/components/`**: 再利用可能なVueコンポーネントを格納
- **`src/views/`**: ページレベルのコンポーネントを格納
- **`src/stores/`**: Piniaを使った状態管理ファイル
- **`src/utils/`**: フロントエンド共通のユーティリティ関数
- **`src/assets/`**: 画像、スタイルシートなどの静的ファイル

#### バックエンド (`backend/`)
- **`app/api/`**: REST APIのエンドポイント定義
- **`app/models/`**: データベースモデルの定義
- **`app/core/`**: アプリケーションの核となる設定や共通機能
- **`app/utils/`**: バックエンド共通のユーティリティ関数

#### ドキュメント (`docs/`)
- **`templates/`**: 国際標準に準拠したドキュメントテンプレート
- **`api/`**: API仕様書とドキュメント
- **`user_manual/`**: エンドユーザー向けマニュアル

## 🚀 セットアップ手順

### 1. 前提条件

以下のソフトウェアがインストールされている必要があります：

- **Node.js** 18.0.0 以降
- **Python** 3.11.0 以降
- **Git**

### 2. リポジトリのクローン

```bash
git clone https://github.com/takahiko217/stack_watcher.git
cd stack_watcher
```

### 3. 自動セットアップ

環境のセットアップは自動化されています：

```bash
# 実行権限を付与
chmod +x scripts/setup.sh

# セットアップスクリプトを実行
./scripts/setup.sh
```

このスクリプトは以下を自動で実行します：
- Node.js と Python の確認
- フロントエンド依存関係のインストール
- Python仮想環境の作成
- バックエンド依存関係のインストール
- 環境設定ファイルの生成

### 4. アプリケーションの起動

```bash
# 実行権限を付与
chmod +x scripts/start.sh

# アプリケーションを起動
./scripts/start.sh
```

### 5. アクセス

セットアップが完了したら、以下のURLでアクセスできます：

- **フロントエンド**: http://localhost:3000
- **バックエンド API**: http://localhost:8000
- **API ドキュメント**: http://localhost:8000/docs

## 🔧 開発環境

### 手動セットアップ（上級者向け）

自動セットアップを使わない場合は、以下の手順で手動セットアップできます：

#### フロントエンド
```bash
cd frontend
npm install
npm run dev
```

#### バックエンド
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### 🧪 テスト実行

```bash
# フロントエンドのテスト
cd frontend
npm run test

# バックエンドのテスト
cd backend
source venv/bin/activate
pytest
```

### 🔍 コード品質チェック

```bash
# フロントエンドのリント
cd frontend
npm run lint

# バックエンドのリント
cd backend
source venv/bin/activate
flake8 .
```

## 📖 ドキュメント

このプロジェクトでは国際標準に準拠したドキュメント管理を採用しています：

- **[README テンプレート](docs/templates/README_template.md)**: プロジェクト概要用
- **[API 仕様書テンプレート](docs/templates/API_specification_template.md)**: REST API仕様用
- **[ユーザーマニュアルテンプレート](docs/templates/user_manual_template.md)**: エンドユーザー向け

## 🎨 コーディングガイドライン

### Vue.js（フロントエンド）
- **ファイル名**: PascalCase（例: `UserProfile.vue`）
- **コンポーネント名**: PascalCase
- **変数・関数名**: camelCase
- **定数**: UPPER_SNAKE_CASE
- **コメント**: 日本語で初心者向けに詳しく記載

### Python（バックエンド）
- **ファイル名**: snake_case（例: `user_service.py`）
- **クラス名**: PascalCase
- **関数・変数名**: snake_case
- **定数**: UPPER_SNAKE_CASE
- **docstring**: 日本語で目的と使用方法を明記

## 🚨 トラブルシューティング

### よくある問題

#### ポートが既に使用されている
```bash
# ポート使用状況の確認
lsof -i :3000  # フロントエンド
lsof -i :8000  # バックエンド

# プロセスを終了
kill -9 [PID]
```

#### 依存関係のエラー
```bash
# フロントエンド
cd frontend
rm -rf node_modules package-lock.json
npm install

# バックエンド
cd backend
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 権限エラー
```bash
# スクリプトに実行権限を付与
chmod +x scripts/*.sh
```

## 🤝 貢献

### 貢献の流れ
1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチをプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

### 開発ルール
- コミットメッセージは日本語で記載
- 新機能には必ずテストを追加
- コードには初心者向けのコメントを記載
- ドキュメントの更新を忘れずに

## 📄 ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 📞 お問い合わせ

- **GitHub Issues**: [Issues ページ](https://github.com/takahiko217/stack_watcher/issues)
- **プロジェクト管理者**: takahiko217

---

## 💡 学習リソース

### 使用技術の学習リンク
- **Vue.js**: [公式ドキュメント](https://vuejs.org/)
- **FastAPI**: [公式ドキュメント](https://fastapi.tiangolo.com/)
- **Python**: [公式チュートリアル](https://docs.python.org/ja/3/tutorial/)
- **JavaScript**: [MDN Web Docs](https://developer.mozilla.org/ja/docs/Web/JavaScript)

### コーディングベストプラクティス
- コードは自己文書化を心がける
- 関数は単一責任の原則に従う
- エラーハンドリングを適切に実装
- セキュリティを常に意識する

**Happy Coding! 🚀**
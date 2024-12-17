# セットアップガイド

## 1. システム要件

### 必須ソフトウェア
- Docker Engine 24.0以上
- Docker Compose 2.22以上
- Git 2.40以上

### 推奨開発環境
- VS Code 1.80以上
- Python 3.11以上（ローカル開発用）
- Node.js 18.x以上（ローカル開発用）

### 必要なリソース
- CPU: 2コア以上
- メモリ: 8GB以上
- ディスク: 10GB以上の空き容量

## 2. 初期セットアップ

### リポジトリのクローン
```bash
git clone [リポジトリURL]
cd project-e
```

### 環境変数の設定

1. バックエンド設定（backend/.env）
```ini
# データベース設定
DATABASE_URL=postgresql://user:pass@db:5432/project_e
POSTGRES_USER=user
POSTGRES_PASSWORD=pass
POSTGRES_DB=project_e

# アプリケーション設定
APP_ENV=development
DEBUG=True
SECRET_KEY=your-secret-key
CORS_ORIGINS=http://localhost:5173

# JWT設定
JWT_SECRET_KEY=your-jwt-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

2. フロントエンド設定（frontend/.env）
```ini
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_ENV=development
```

### Dockerコンテナの構築と起動
```bash
# イメージのビルド
docker-compose build

# コンテナの起動
docker-compose up -d
```

## 3. データベースのセットアップ

### マイグレーションの実行
```bash
# バックエンドコンテナに入る
docker-compose exec backend bash

# マイグレーション実行
python -m alembic upgrade head
```

### テストデータの投入
```bash
# バックエンドコンテナ内で実行
python -m app.scripts.seed_data
```

## 4. 開発環境の設定

### VSCode拡張機能のインストール

1. Python開発用
- Python
- Pylance
- Python Test Explorer
- autoDocstring
- Black Formatter

2. TypeScript/React開発用
- ESLint
- Prettier
- ES7+ React/Redux/React-Native snippets
- Tailwind CSS IntelliSense

### VSCode設定（.vscode/settings.json）
```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": null,
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  },
  "[typescript][javascript][typescriptreact][javascriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  },
  "python.analysis.typeCheckingMode": "basic",
  "python.testing.pytestEnabled": true
}
```

## 5. 動作確認

### ヘルスチェック
```bash
curl http://localhost:8000/health
```

期待されるレスポンス：
```json
{
  "status": "healthy",
  "timestamp": "2024-12-17T10:00:00.000Z"
}
```

### Swagger UI
ブラウザで以下のURLにアクセス：
- http://localhost:8000/docs

### フロントエンド
ブラウザで以下のURLにアクセス：
- http://localhost:5173

## 6. トラブルシューティング

### よくある問題と解決方法

1. データベース接続エラー
```bash
# ログの確認
docker-compose logs db

# DBコンテナの再起動
docker-compose restart db

# DB初期化（データは失われます）
docker-compose down -v
docker-compose up -d
```

2. ポートの競合
```bash
# 使用中のポートの確認
netstat -an | grep 5173
netstat -an | grep 8000
netstat -an | grep 5432

# 該当のプロセスを終了するか、docker-compose.ymlでポートを変更
```

3. パッケージのインストールエラー
```bash
# キャッシュのクリア
# フロントエンド
docker-compose exec frontend pnpm clean
docker-compose exec frontend pnpm install

# バックエンド
docker-compose exec backend poetry lock --no-update
docker-compose exec backend poetry install
```

4. コンテナの起動に失敗する場合
```bash
# コンテナのログを確認
docker-compose logs

# コンテナを再ビルド
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 7. 開発用コマンド集

### バックエンド開発

```bash
# テストの実行
docker-compose exec backend pytest

# コードフォーマット
docker-compose exec backend black .

# 型チェック
docker-compose exec backend mypy .

# 依存関係の追加
docker-compose exec backend poetry add package-name

# マイグレーションの作成
docker-compose exec backend alembic revision --autogenerate -m "description"
```

### フロントエンド開発

```bash
# 依存関係の追加
docker-compose exec frontend pnpm add package-name

# ビルド
docker-compose exec frontend pnpm build

# リント
docker-compose exec frontend pnpm lint

# テスト
docker-compose exec frontend pnpm test

# タイプチェック
docker-compose exec frontend pnpm type-check
```

## 8. 開発フロー

1. 新機能の開発
```bash
# 新しいブランチの作成
git checkout -b feature/new-feature

# 開発作業
git add .
git commit -m "feat: implement new feature"

# プッシュ
git push origin feature/new-feature
```

2. テストの実行
```bash
# バックエンドテスト
docker-compose exec backend pytest

# フロントエンドテスト
docker-compose exec frontend pnpm test
```

3. コードレビュー
- プルリクエストの作成
- レビュー依頼
- レビューコメントの対応
- 承認後マージ

## 9. サポート

### ドキュメント
- [システム構成書](../technical/system.md)
- [API仕様書](../technical/api.md)
- [データベース設計書](../technical/database.md)

### 問題報告
- Issueの作成
- バグレポートテンプレートの使用
- 再現手順の記載

### 定期メンテナンス
- 依存パッケージの更新
- セキュリティパッチの適用
- バックアップの確認
# Engineer Project Management System

エンジニア、案件、営業担当者の管理および最適なマッチングを実現するシステム

## プロジェクト概要

### 目的
- エンジニアのスキルと案件要件のマッチング効率化
- プロジェクト管理の効率化
- エンジニアと営業のコミュニケーション円滑化

### 主な機能
- エンジニア情報の管理
- プロジェクト情報の管理
- 営業担当者情報の管理
- スキルベースのマッチング
- ステータス管理・追跡

## 技術スタック

### フロントエンド
- React 18.x
- TypeScript 5.x
- Vite
- Tailwind CSS

### バックエンド
- FastAPI (Python 3.11)
- PostgreSQL 15
- SQLAlchemy (ORM)
- Docker/Docker Compose

## クイックスタート

1. リポジトリのクローン:
```bash
git clone [リポジトリURL]
cd project-e
```

2. 環境変数の設定:
```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

3. 開発環境の起動:
```bash
docker-compose up -d
```

4. データベースのセットアップ:
```bash
docker-compose exec backend bash
python -m app.scripts.create_tables
python -m app.scripts.seed_data
```

5. アクセス:
- フロントエンド: http://localhost:5173
- バックエンドAPI: http://localhost:8000
- API ドキュメント: http://localhost:8000/docs

## ドキュメント

詳細なドキュメントは `docs/` ディレクトリを参照してください：

```
docs/
├── technical/           # 技術仕様書
│   ├── api.md          # API仕様書
│   ├── database.md     # データベース設計書
│   └── system.md       # システム構成書
│
└── guides/             # ガイド
    ├── setup.md        # セットアップガイド
    ├── development.md  # 開発ガイド
    └── operation.md    # 運用ガイド
```

セットアップの詳細な手順については、[セットアップガイド](docs/guides/setup.md)を参照してください。
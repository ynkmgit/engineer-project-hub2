# エンジニア・営業案件管理システム 開発仕様書

## 1. システム概要

### 1.1 開発目的
エンジニア、案件、営業担当者の管理および最適なマッチングを実現するシステム

### 1.2 開発スコープ（Phase 1）
- エンジニア基本情報管理
- 案件基本情報管理
- 営業担当者管理
- 基本的なマッチング機能
- 検索機能

## 2. 技術スタック

### 2.1 フロントエンド
```bash
# コア技術
- React 18
- TypeScript 5.x
- Vite
- TanStack Query v5
- React Router v6
- Tailwind CSS

# 開発環境
- Node.js 18.x以上
- pnpm（パッケージマネージャー）
```

### 2.2 バックエンド
```bash
# コア技術
- FastAPI
- Python 3.11以上
- SQLAlchemy
- Pydantic
- Uvicorn

# 開発環境
- Python 3.11
- Poetry（パッケージマネージャー）
```

### 2.3 データベース
- PostgreSQL 14以上

## 3. API仕様

### 3.1 エンドポイント一覧
```python
# エンジニア関連
GET     /api/v1/engineers           # エンジニア一覧取得
POST    /api/v1/engineers           # エンジニア登録
GET     /api/v1/engineers/{id}      # エンジニア詳細取得
PUT     /api/v1/engineers/{id}      # エンジニア情報更新
DELETE  /api/v1/engineers/{id}      # エンジニア削除

# 案件関連
GET     /api/v1/projects            # 案件一覧取得
POST    /api/v1/projects            # 案件登録
GET     /api/v1/projects/{id}       # 案件詳細取得
PUT     /api/v1/projects/{id}       # 案件情報更新
DELETE  /api/v1/projects/{id}       # 案件削除

# 営業担当者関連
GET     /api/v1/sales               # 営業担当者一覧取得
POST    /api/v1/sales               # 営業担当者登録
GET     /api/v1/sales/{id}          # 営業担当者詳細取得
PUT     /api/v1/sales/{id}          # 営業担当者情報更新
DELETE  /api/v1/sales/{id}          # 営業担当者削除

# マッチング関連
GET     /api/v1/matching            # マッチング結果取得
POST    /api/v1/matching/calculate  # マッチング計算実行
```

### 3.2 データモデル
```typescript
// エンジニア
interface Engineer {
  id: number;
  name: string;
  email: string;
  phone: string;
  skills: string[];
  status: 'available' | 'working';
  availableDate: string;
  created_at: string;
  updated_at: string;
}

// 案件
interface Project {
  id: number;
  name: string;
  description: string;
  required_skills: string[];
  start_date: string;
  end_date: string;
  status: 'new' | 'in_progress' | 'completed';
  sales_id: number;
  created_at: string;
  updated_at: string;
}

// 営業担当者
interface SalesPerson {
  id: number;
  name: string;
  email: string;
  phone: string;
  created_at: string;
  updated_at: string;
}
```

## 4. データベース設計

### 4.1 テーブル定義
```sql
-- エンジニアテーブル
CREATE TABLE engineers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20),
    skills JSONB,
    status VARCHAR(20) NOT NULL,
    available_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 案件テーブル
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    required_skills JSONB,
    start_date DATE,
    end_date DATE,
    status VARCHAR(20) NOT NULL,
    sales_id INTEGER REFERENCES sales_staff(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 営業担当者テーブル
CREATE TABLE sales_staff (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

## 5. 開発環境セットアップ

### 5.1 必要な環境変数
```bash
# .env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
JWT_SECRET=your-secret-key
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:5173
```

### 5.2 開発環境構築手順
```bash
# バックエンド
$ cd backend
$ poetry install
$ poetry run uvicorn main:app --reload

# フロントエンド
$ cd frontend
$ pnpm install
$ pnpm dev

# データベース
$ docker compose up -d db
```

## 6. 実装ガイドライン

### 6.1 コーディング規約
- ESLint/Prettierの設定に従う
- 型定義は明示的に行う
- コンポーネントは機能単位で分割する
- カスタムフックを活用する
- APIクライアントは集約する

### 6.2 コードサンプル
```typescript
// APIクライアントの例
import axios from 'axios';

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// カスタムフックの例
export function useEngineers() {
  return useQuery({
    queryKey: ['engineers'],
    queryFn: () => api.get('/engineers').then(res => res.data),
  });
}
```

## 7. 開発フロー

### 7.1 ブランチ戦略
```bash
main        # プロダクション環境
develop     # 開発環境
feature/*   # 機能開発
fix/*       # バグ修正
```

### 7.2 コミットメッセージ規約
```bash
feat: 新機能
fix: バグ修正
docs: ドキュメント
style: コードスタイル
refactor: リファクタリング
test: テストコード
chore: ビルド・補助ツール
```

## 8. テスト要件

### 8.1 ユニットテスト
- コンポーネントのテスト
- カスタムフックのテスト
- ユーティリティ関数のテスト

### 8.2 E2Eテスト
- ユーザーフローのテスト
- API統合テスト
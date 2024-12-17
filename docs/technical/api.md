# API仕様書

## 1. 概要

### ベース情報
- ベースURL: `http://localhost:8000`
- 認証方式: JWT Bearer Token
- レスポンス形式: JSON
- 文字コード: UTF-8

### 共通ヘッダー
```
Content-Type: application/json
Authorization: Bearer <token>  # 認証が必要なエンドポイントの場合
```

### 共通レスポンス形式

#### 成功時
```json
{
  "data": {
    // レスポンスデータ
  },
  "meta": {
    "page": 1,          // ページング情報（該当する場合）
    "per_page": 25,
    "total": 100
  }
}
```

#### エラー時
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "エラーメッセージ",
    "details": {
      // 詳細情報（該当する場合）
    }
  }
}
```

## 2. 認証API

### ログイン
```
POST /auth/login
```

リクエスト：
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

レスポンス：
```json
{
  "data": {
    "access_token": "eyJ0eXAi...",
    "token_type": "bearer",
    "expires_in": 3600
  }
}
```

## 3. エンジニアAPI

### エンジニア一覧取得
```
GET /api/v1/engineers
```

クエリパラメータ：
| パラメータ | 型 | 必須 | 説明 |
|------------|-----|------|------|
| page | integer | No | ページ番号（デフォルト: 1）|
| per_page | integer | No | 1ページの件数（デフォルト: 25）|
| status | string | No | ステータスでフィルタ |
| skills | string[] | No | スキルでフィルタ |

レスポンス：
```json
{
  "data": [
    {
      "id": 1,
      "name": "山田太郎",
      "email": "yamada@example.com",
      "phone": "090-1234-5678",
      "skills": {
        "languages": ["Python", "JavaScript"],
        "frameworks": ["FastAPI", "React"],
        "databases": ["PostgreSQL"]
      },
      "status": "稼働可能",
      "available_date": "2025-01-01"
    }
  ],
  "meta": {
    "page": 1,
    "per_page": 25,
    "total": 100
  }
}
```

### エンジニア詳細取得
```
GET /api/v1/engineers/{id}
```

レスポンス：
```json
{
  "data": {
    "id": 1,
    "name": "山田太郎",
    "email": "yamada@example.com",
    "phone": "090-1234-5678",
    "skills": {
      "languages": ["Python", "JavaScript"],
      "frameworks": ["FastAPI", "React"],
      "databases": ["PostgreSQL"]
    },
    "status": "稼働可能",
    "available_date": "2025-01-01",
    "projects": [
      {
        "id": 1,
        "name": "プロジェクトA",
        "start_date": "2024-01-01",
        "end_date": "2024-06-30",
        "status": "進行中"
      }
    ]
  }
}
```

### エンジニア新規登録
```
POST /api/v1/engineers
```

リクエスト：
```json
{
  "name": "新規エンジニア",
  "email": "new@example.com",
  "phone": "090-0000-0000",
  "skills": {
    "languages": ["Python", "JavaScript"],
    "frameworks": ["FastAPI", "React"],
    "databases": ["PostgreSQL"]
  },
  "status": "稼働可能",
  "available_date": "2025-01-01"
}
```

レスポンス：
```json
{
  "data": {
    "id": 2,
    "name": "新規エンジニア",
    "email": "new@example.com",
    "phone": "090-0000-0000",
    "skills": {
      "languages": ["Python", "JavaScript"],
      "frameworks": ["FastAPI", "React"],
      "databases": ["PostgreSQL"]
    },
    "status": "稼働可能",
    "available_date": "2025-01-01"
  }
}
```

## 4. プロジェクトAPI

### プロジェクト一覧取得
```
GET /api/v1/projects
```

クエリパラメータ：
| パラメータ | 型 | 必須 | 説明 |
|------------|-----|------|------|
| page | integer | No | ページ番号 |
| per_page | integer | No | 1ページの件数 |
| status | string | No | ステータスでフィルタ |
| skills | string[] | No | 必要スキルでフィルタ |

レスポンス：
```json
{
  "data": [
    {
      "id": 1,
      "name": "プロジェクトA",
      "description": "プロジェクトの説明",
      "required_skills": {
        "must": {
          "languages": ["Python"],
          "frameworks": ["FastAPI"],
          "databases": ["PostgreSQL"]
        },
        "preferred": {
          "languages": ["JavaScript"],
          "frameworks": ["React"]
        }
      },
      "start_date": "2024-01-01",
      "end_date": "2024-06-30",
      "status": "準備中",
      "sales_staff": {
        "id": 1,
        "name": "営業担当者A"
      }
    }
  ],
  "meta": {
    "page": 1,
    "per_page": 25,
    "total": 50
  }
}
```

### プロジェクト詳細取得
```
GET /api/v1/projects/{id}
```

レスポンス：
```json
{
  "data": {
    "id": 1,
    "name": "プロジェクトA",
    "description": "プロジェクトの説明",
    "required_skills": {
      "must": {
        "languages": ["Python"],
        "frameworks": ["FastAPI"],
        "databases": ["PostgreSQL"]
      },
      "preferred": {
        "languages": ["JavaScript"],
        "frameworks": ["React"]
      }
    },
    "start_date": "2024-01-01",
    "end_date": "2024-06-30",
    "status": "準備中",
    "sales_staff": {
      "id": 1,
      "name": "営業担当者A"
    },
    "assigned_engineers": [
      {
        "id": 1,
        "name": "山田太郎",
        "skills": {
          "languages": ["Python", "JavaScript"],
          "frameworks": ["FastAPI", "React"]
        }
      }
    ]
  }
}
```

## 5. マッチングAPI

### マッチング候補取得
```
GET /api/v1/matching/projects/{project_id}/candidates
```

レスポンス：
```json
{
  "data": [
    {
      "engineer": {
        "id": 1,
        "name": "山田太郎",
        "skills": {
          "languages": ["Python", "JavaScript"],
          "frameworks": ["FastAPI", "React"]
        },
        "status": "稼働可能",
        "available_date": "2025-01-01"
      },
      "matching_score": 0.85,
      "matching_details": {
        "must_have_skills": ["Python", "FastAPI"],
        "preferred_skills": ["JavaScript", "React"],
        "missing_skills": []
      }
    }
  ],
  "meta": {
    "page": 1,
    "per_page": 25,
    "total": 10
  }
}
```

### アサイン登録
```
POST /api/v1/matching/assignments
```

リクエスト：
```json
{
  "project_id": 1,
  "engineer_id": 1,
  "start_date": "2024-01-01",
  "end_date": "2024-06-30"
}
```

レスポンス：
```json
{
  "data": {
    "id": 1,
    "project": {
      "id": 1,
      "name": "プロジェクトA"
    },
    "engineer": {
      "id": 1,
      "name": "山田太郎"
    },
    "start_date": "2024-01-01",
    "end_date": "2024-06-30",
    "status": "予定"
  }
}
```

## 6. エラーコード一覧

| コード | 説明 |
|--------|------|
| AUTH_001 | 認証エラー |
| AUTH_002 | トークン期限切れ |
| USER_001 | ユーザーが存在しない |
| USER_002 | メールアドレスが重複 |
| PROJ_001 | プロジェクトが存在しない |
| PROJ_002 | 無効なプロジェクト状態 |
| MATCH_001 | アサイン期間の重複 |
| MATCH_002 | エンジニアが稼働不可 |

## 7. ステータス定義

### エンジニアステータス
- 稼働可能
- 案件中
- 調整中
- 休暇中
- 退会

### プロジェクトステータス
- 準備中
- 調整中
- 進行中
- 完了
- 中断
- キャンセル

### アサインメントステータス
- 予定
- 確定
- キャンセル
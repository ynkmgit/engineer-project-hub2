# 開発ガイド

[前半部分は省略...]

## 4. パフォーマンス最適化

### バックエンド最適化

#### 1. データベースクエリ
```python
# クエリの最適化例
async def get_engineers_with_projects():
    # Bad: N+1問題
    engineers = await Engineer.all()
    for engineer in engineers:
        await engineer.projects.all()

    # Good: プリフェッチを使用
    engineers = await Engineer.all().prefetch_related('projects')
```

#### 2. キャッシュの活用
```python
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

@router.get("/engineers/", response_model=List[EngineerResponse])
@cache(expire=300)  # 5分間キャッシュ
async def list_engineers():
    return await Engineer.all()
```

#### 3. 非同期処理
```python
async def process_large_data():
    tasks = []
    for item in data:
        task = asyncio.create_task(process_item(item))
        tasks.append(task)
    
    results = await asyncio.gather(*tasks)
    return results
```

### フロントエンド最適化

#### 1. メモ化
```typescript
// コンポーネントのメモ化
const EngineerCard = React.memo<EngineerCardProps>(({ 
  engineer,
  onSelect 
}) => {
  return (
    // ...component implementation
  );
});

// 関数のメモ化
const calculateScore = useMemo(() => {
  return complexCalculation(engineer.skills, project.requirements);
}, [engineer.skills, project.requirements]);
```

#### 2. 遅延ローディング
```typescript
// ルートレベルでの遅延ローディング
const ProjectDetails = lazy(() => 
  import('./components/ProjectDetails')
);

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <ProjectDetails />
    </Suspense>
  );
}
```

#### 3. 仮想スクロール
```typescript
import { VirtualList } from 'react-window';

function EngineerList({ engineers }) {
  const Row = ({ index, style }) => (
    <div style={style}>
      <EngineerCard engineer={engineers[index]} />
    </div>
  );

  return (
    <VirtualList
      height={500}
      itemCount={engineers.length}
      itemSize={100}
      width="100%"
    >
      {Row}
    </VirtualList>
  );
}
```

## 5. セキュリティ対策

### バックエンドセキュリティ

#### 1. 入力バリデーション
```python
from pydantic import BaseModel, EmailStr, constr

class EngineerCreate(BaseModel):
    name: constr(min_length=1, max_length=100)
    email: EmailStr
    phone: constr(regex=r'^\d{2,4}-\d{2,4}-\d{4}$')
```

#### 2. JWT認証
```python
from fastapi_jwt_auth import AuthJWT

@router.post("/login")
async def login(
    credentials: LoginCredentials,
    Authorize: AuthJWT = Depends()
):
    user = await authenticate_user(credentials)
    access_token = Authorize.create_access_token(subject=user.id)
    return {"access_token": access_token}
```

#### 3. CORS設定
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### フロントエンドセキュリティ

#### 1. XSS対策
```typescript
// テキストのエスケープ
const sanitizeText = (text: string) => {
  return text.replace(/[&<>"']/g, (match) => {
    const escape: { [key: string]: string } = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;'
    };
    return escape[match];
  });
};
```

#### 2. CSRF対策
```typescript
// APIリクエストにCSRFトークンを含める
const api = axios.create({
  baseURL: '/api',
  headers: {
    'X-CSRF-TOKEN': getCsrfToken(),
  },
  withCredentials: true
});
```

## 6. エラー処理

### バックエンドエラー処理

#### 1. カスタム例外
```python
class ProjectException(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(message)

@app.exception_handler(ProjectException)
async def project_exception_handler(
    request: Request,
    exc: ProjectException
):
    return JSONResponse(
        status_code=400,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message
            }
        }
    )
```

#### 2. エラーログ
```python
import logging

logger = logging.getLogger(__name__)

@router.post("/projects/")
async def create_project(project: ProjectCreate):
    try:
        return await ProjectService.create(project)
    except Exception as e:
        logger.error(f"Failed to create project: {e}", exc_info=True)
        raise ProjectException(
            code="PROJECT_CREATE_ERROR",
            message="プロジェクトの作成に失敗しました"
        )
```

### フロントエンドエラー処理

#### 1. エラーバウンダリ
```typescript
class ErrorBoundary extends React.Component {
  state = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error('Error caught by boundary:', error, info);
  }

  render() {
    if (this.state.hasError) {
      return <ErrorDisplay error={this.state.error} />;
    }
    return this.props.children;
  }
}
```

#### 2. APIエラー処理
```typescript
const useAPI = <T,>(url: string) => {
  const [state, setState] = useState<{
    data: T | null;
    loading: boolean;
    error: Error | null;
  }>({
    data: null,
    loading: true,
    error: null,
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get<T>(url);
        setState({
          data: response.data,
          loading: false,
          error: null,
        });
      } catch (e) {
        setState({
          data: null,
          loading: false,
          error: e as Error,
        });
      }
    };

    fetchData();
  }, [url]);

  return state;
};
```

## 7. CI/CD

### GitHub Actions設定例
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      # バックエンドテスト
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Run Backend Tests
        run: |
          cd backend
          pip install poetry
          poetry install
          poetry run pytest
      
      # フロントエンドテスト
      - name: Set up Node
        uses: actions/setup-node@v2
        with:
          node-version: '18'
      
      - name: Run Frontend Tests
        run: |
          cd frontend
          pnpm install
          pnpm test

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Production
        run: |
          # デプロイ手順をここに記述
```

## 8. モニタリング

### アプリケーションログ
```python
# structured logging
import structlog

logger = structlog.get_logger()

logger.info(
    "project_created",
    project_id=project.id,
    user_id=user.id,
    timestamp=datetime.utcnow()
)
```

### メトリクス収集
```python
from prometheus_client import Counter, Histogram

request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_latency = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)
```

## 9. ドキュメント生成

### OpenAPI (Swagger)
```python
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Engineer Project Management API",
        version="1.0.0",
        description="エンジニアプロジェクト管理システムのAPI仕様",
        routes=app.routes,
    )
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

### TSDoc/JSDoc
```typescript
/**
 * エンジニアとプロジェクトのマッチングスコアを計算する
 * @param engineer - エンジニア情報
 * @param project - プロジェクト情報
 * @returns マッチングスコア（0-1の範囲）
 */
function calculateMatchingScore(
  engineer: Engineer,
  project: Project
): number {
  // 実装
}
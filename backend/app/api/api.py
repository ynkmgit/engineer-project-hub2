from fastapi import APIRouter
from .endpoints import projects

api_router = APIRouter()

# プロジェクト関連のエンドポイントを登録
api_router.include_router(
    projects.router,
    prefix="/projects",
    tags=["projects"]
)
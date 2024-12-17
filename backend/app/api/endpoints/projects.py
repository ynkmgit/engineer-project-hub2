from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ...crud import project as project_crud
from ...schemas.project import Project, ProjectCreate, ProjectUpdate
from ...database import get_db

router = APIRouter()

@router.get("/", response_model=List[Project])
def read_projects(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    プロジェクト一覧を取得する。
    ステータスでフィルタリング可能。
    """
    projects = project_crud.get_projects(db, skip=skip, limit=limit, status=status)
    return projects

@router.post("/", response_model=Project)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    """
    新規プロジェクトを作成する。
    """
    return project_crud.create_project(db=db, project=project)

@router.get("/{project_id}", response_model=Project)
def read_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """
    特定のプロジェクトの詳細を取得する。
    """
    db_project = project_crud.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@router.put("/{project_id}", response_model=Project)
def update_project(
    project_id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db)
):
    """
    プロジェクト情報を更新する。
    """
    db_project = project_crud.update_project(db, project_id=project_id, project=project)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """
    プロジェクトを削除する。
    """
    success = project_crud.delete_project(db, project_id=project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"status": "success", "message": "Project deleted"}
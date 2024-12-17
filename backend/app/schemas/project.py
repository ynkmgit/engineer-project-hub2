from datetime import date
from typing import Optional, Dict, List
from pydantic import BaseModel

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    required_skills: Optional[Dict[str, List[str]]] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: str
    sales_id: int

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    name: Optional[str] = None
    status: Optional[str] = None
    sales_id: Optional[int] = None

class Project(ProjectBase):
    id: int
    created_at: date
    updated_at: Optional[date] = None

    class Config:
        from_attributes = True
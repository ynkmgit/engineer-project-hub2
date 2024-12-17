from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime

class EngineerBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    skills: List[str]
    status: str
    available_date: Optional[date] = None

class EngineerCreate(EngineerBase):
    pass

class Engineer(EngineerBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    required_skills: List[str]
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: str
    sales_id: int

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class SalesStaffBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None

class SalesStaffCreate(SalesStaffBase):
    pass

class SalesStaff(SalesStaffBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
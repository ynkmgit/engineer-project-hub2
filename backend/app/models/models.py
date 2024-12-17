from sqlalchemy import Column, Integer, String, Date, ForeignKey, ARRAY, JSON, DateTime
from sqlalchemy.sql import func
from ..database import Base

class Engineer(Base):
    __tablename__ = "engineers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20))
    skills = Column(JSON)
    status = Column(String(20), nullable=False)
    available_date = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(String)
    required_skills = Column(JSON)
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String(20), nullable=False)
    sales_id = Column(Integer, ForeignKey("sales_staff.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class SalesStaff(Base):
    __tablename__ = "sales_staff"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
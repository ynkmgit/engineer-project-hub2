from sqlalchemy.orm import Session
from ..models.models import Engineer
from ..schemas.schemas import EngineerCreate
from typing import List

def get_engineer(db: Session, engineer_id: int):
    return db.query(Engineer).filter(Engineer.id == engineer_id).first()

def get_engineer_by_email(db: Session, email: str):
    return db.query(Engineer).filter(Engineer.email == email).first()

def get_engineers(db: Session, skip: int = 0, limit: int = 100) -> List[Engineer]:
    return db.query(Engineer).offset(skip).limit(limit).all()

def create_engineer(db: Session, engineer: EngineerCreate):
    db_engineer = Engineer(
        name=engineer.name,
        email=engineer.email,
        phone=engineer.phone,
        skills=engineer.skills,
        status=engineer.status,
        available_date=engineer.available_date
    )
    db.add(db_engineer)
    db.commit()
    db.refresh(db_engineer)
    return db_engineer

def update_engineer(db: Session, engineer_id: int, engineer: EngineerCreate):
    db_engineer = db.query(Engineer).filter(Engineer.id == engineer_id).first()
    if db_engineer:
        for key, value in engineer.dict().items():
            setattr(db_engineer, key, value)
        db.commit()
        db.refresh(db_engineer)
    return db_engineer

def delete_engineer(db: Session, engineer_id: int):
    db_engineer = db.query(Engineer).filter(Engineer.id == engineer_id).first()
    if db_engineer:
        db.delete(db_engineer)
        db.commit()
        return True
    return False
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..crud import crud_engineer
from ..schemas.schemas import Engineer, EngineerCreate
from ..database import get_db

router = APIRouter()

@router.get("/engineers/", response_model=List[Engineer])
def read_engineers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    engineers = crud_engineer.get_engineers(db, skip=skip, limit=limit)
    return engineers

@router.post("/engineers/", response_model=Engineer)
def create_engineer(engineer: EngineerCreate, db: Session = Depends(get_db)):
    db_engineer = crud_engineer.get_engineer_by_email(db, email=engineer.email)
    if db_engineer:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_engineer.create_engineer(db=db, engineer=engineer)

@router.get("/engineers/{engineer_id}", response_model=Engineer)
def read_engineer(engineer_id: int, db: Session = Depends(get_db)):
    db_engineer = crud_engineer.get_engineer(db, engineer_id=engineer_id)
    if db_engineer is None:
        raise HTTPException(status_code=404, detail="Engineer not found")
    return db_engineer

@router.put("/engineers/{engineer_id}", response_model=Engineer)
def update_engineer(engineer_id: int, engineer: EngineerCreate, db: Session = Depends(get_db)):
    db_engineer = crud_engineer.update_engineer(db, engineer_id=engineer_id, engineer=engineer)
    if db_engineer is None:
        raise HTTPException(status_code=404, detail="Engineer not found")
    return db_engineer

@router.delete("/engineers/{engineer_id}")
def delete_engineer(engineer_id: int, db: Session = Depends(get_db)):
    success = crud_engineer.delete_engineer(db, engineer_id=engineer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Engineer not found")
    return {"status": "success", "message": "Engineer deleted"}
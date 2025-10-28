
# routes/students.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import models, schemas
from werkzeug.security import generate_password_hash, check_password_hash

router = APIRouter(prefix="/students", tags=["students"])

@router.post("/", response_model=schemas.StudentOut, status_code=status.HTTP_201_CREATED)
def create_student(student_in: schemas.StudentCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Student).filter(models.Student.email == student_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = generate_password_hash(student_in.password)
    student = models.Student(name=student_in.name, email=student_in.email, hashed_password=hashed)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

@router.get("/", response_model=List[schemas.StudentOut])
def list_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = db.query(models.Student).offset(skip).limit(limit).all()
    return students


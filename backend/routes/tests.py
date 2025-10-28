# routes/tests.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import models, schemas

router = APIRouter(prefix="/tests", tags=["tests"])

@router.post("/", response_model=schemas.TestOut, status_code=status.HTTP_201_CREATED)
def create_test(test_in: schemas.TestCreate, db: Session = Depends(get_db)):
    test = models.Test(title=test_in.title, description=test_in.description, total_marks=test_in.total_marks)
    db.add(test)
    db.commit()
    db.refresh(test)
    # Add questions if provided
    if test_in.questions:
        for q in test_in.questions:
            question = models.Question(
                test_id=test.id,
                text=q.text,
                option_a=q.option_a,
                option_b=q.option_b,
                option_c=q.option_c,
                option_d=q.option_d,
                correct_option=q.correct_option,
                marks=q.marks
            )
            db.add(question)
        db.commit()
        db.refresh(test)
    return test

@router.get("/", response_model=List[schemas.TestOut])
def list_tests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tests = db.query(models.Test).offset(skip).limit(limit).all()
    return tests

@router.get("/{test_id}", response_model=schemas.TestOut)
def get_test(test_id: int, db: Session = Depends(get_db)):
    test = db.query(models.Test).filter(models.Test.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    return test

@router.put("/{test_id}", response_model=schemas.TestOut)
def update_test(test_id: int, test_in: schemas.TestCreate, db: Session = Depends(get_db)):
    test = db.query(models.Test).filter(models.Test.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    test.title = test_in.title
    test.description = test_in.description
    test.total_marks = test_in.total_marks
    db.commit()
    db.refresh(test)
    return test

@router.delete("/{test_id}")
def delete_test(test_id: int, db: Session = Depends(get_db)):
    test = db.query(models.Test).filter(models.Test.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    db.delete(test)
    db.commit()
    return {"message": "Test deleted"}

@router.post("/{test_id}/questions", response_model=schemas.QuestionOut, status_code=status.HTTP_201_CREATED)
def add_question(test_id: int, question_in: schemas.QuestionCreate, db: Session = Depends(get_db)):
    test = db.query(models.Test).filter(models.Test.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    question = models.Question(
        test_id=test_id,
        text=question_in.text,
        option_a=question_in.option_a,
        option_b=question_in.option_b,
        option_c=question_in.option_c,
        option_d=question_in.option_d,
        correct_option=question_in.correct_option,
        marks=question_in.marks
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return question

@router.get("/{test_id}/questions", response_model=List[schemas.QuestionOut])
def list_questions(test_id: int, db: Session = Depends(get_db)):
    questions = db.query(models.Question).filter(models.Question.test_id == test_id).all()
    return questions

@router.post("/attempts", response_model=schemas.AttemptOut, status_code=status.HTTP_201_CREATED)
def create_attempt(attempt_in: schemas.AttemptCreate, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == attempt_in.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    test = db.query(models.Test).filter(models.Test.id == attempt_in.test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    attempt = models.Attempt(student_id=attempt_in.student_id, test_id=attempt_in.test_id)
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt

@router.put("/attempts/{attempt_id}", response_model=schemas.AttemptOut)
def update_attempt(attempt_id: int, score: int, finished: bool, db: Session = Depends(get_db)):
    attempt = db.query(models.Attempt).filter(models.Attempt.id == attempt_id).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    attempt.score = score
    attempt.finished = finished
    db.commit()
    db.refresh(attempt)
    return attempt

@router.get("/attempts/{test_id}/results", response_model=List[schemas.AttemptResult])
def get_test_results(test_id: int, db: Session = Depends(get_db)):
    attempts = db.query(models.Attempt).join(models.Student).join(models.Test).filter(models.Attempt.test_id == test_id, models.Attempt.finished == True).order_by(models.Attempt.score.desc()).all()
    results = []
    rank = 1
    for attempt in attempts:
        result = schemas.AttemptResult(
            id=attempt.id,
            student_name=attempt.student.name,
            test_title=attempt.test.title,
            score=attempt.score,
            created_at=attempt.created_at,
            rank=rank
        )
        results.append(result)
        rank += 1
    return results

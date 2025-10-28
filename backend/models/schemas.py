

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class StudentBase(BaseModel):
    name: str
    email: EmailStr

class StudentCreate(StudentBase):
    password: str

class StudentOut(StudentBase):
    id: int
    class Config:
        from_attributes = True

class QuestionBase(BaseModel):
    text: str
    option_a: Optional[str] = None
    option_b: Optional[str] = None
    option_c: Optional[str] = None
    option_d: Optional[str] = None
    marks: Optional[int] = 1

class QuestionCreate(QuestionBase):
    correct_option: Optional[str] = None

class QuestionOut(QuestionBase):
    id: int
    correct_option: Optional[str] = None
    class Config:
        from_attributes = True

class TestBase(BaseModel):
    title: str
    description: Optional[str] = None

class TestCreate(TestBase):
    total_marks: Optional[int] = 0
    questions: Optional[List[QuestionCreate]] = []

class TestOut(TestBase):
    id: int
    total_marks: int
    questions: List[QuestionOut] = []
    class Config:
        from_attributes = True

class AttemptCreate(BaseModel):
    student_id: int
    test_id: int

class AttemptOut(BaseModel):
    id: int
    student_id: int
    test_id: int
    score: int
    finished: bool
    created_at: datetime
    class Config:
        from_attributes = True

class AttemptResult(BaseModel):
    id: int
    student_name: str
    test_title: str
    score: int
    created_at: datetime
    rank: int
    class Config:
        from_attributes = True




from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from ..database import Base
import datetime

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(200), unique=True, index=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)

    attempts = relationship("Attempt", back_populates="student")

class Test(Base):
    __tablename__ = "tests"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    total_marks = Column(Integer, default=0)

    questions = relationship("Question", back_populates="test")
    attempts = relationship("Attempt", back_populates="test")

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    text = Column(Text, nullable=False)
    option_a = Column(String(300))
    option_b = Column(String(300))
    option_c = Column(String(300))
    option_d = Column(String(300))
    correct_option = Column(String(10))
    marks = Column(Integer, default=1)

    test = relationship("Test", back_populates="questions")

class Attempt(Base):
    __tablename__ = "attempts"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    score = Column(Integer, default=0)
    finished = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("Student", back_populates="attempts")
    test = relationship("Test", back_populates="attempts")


import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from .database import engine, Base
from .routes import students, tests

load_dotenv()

# create DB tables (for dev). Use alembic in production.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Exam Portal API", version="1.0")

# Add CORS middleware to allow frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(students.router)
app.include_router(tests.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Student Exam Portal API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}



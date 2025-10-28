# Exam Portal

A FastAPI-based backend for a student exam portal, designed for easy deployment and frontend integration.

## Features

- Student management (registration, authentication)
- Test creation and management
- Question management with multiple choice options
- Attempt tracking and results
- CORS enabled for frontend integration
- Environment-based configuration

## Setup

1. Clone the repository.
2. Install dependencies:
   ```
   pip install -r backend/requirements.txt
   ```
3. Copy `.env.example` to `.env` and configure your settings:
   ```
   cp .env.example .env
   ```
   Edit `.env` with your desired configuration.

4. Run the application:
   ```
   python main.py
   ```

## Environment Variables

- `DATABASE_URL`: Database connection string (default: SQLite)
- `HOST`: Server host (default: 127.0.0.1)
- `PORT`: Server port (default: 8000)
- `RELOAD`: Enable auto-reload for development (default: true)

## Deployment

For production deployment:

1. Set `RELOAD=false` in your environment.
2. Use a production WSGI server like Gunicorn with Uvicorn workers:
   ```
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```
3. Or use Docker (create a Dockerfile and docker-compose.yml as needed).

## API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.

## CORS Configuration

CORS is enabled with `allow_origins=["*"]` for development. In production, specify allowed origins in your environment or update the middleware in `backend/main.py`.

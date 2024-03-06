# Whelp-Task-FastAPI

Following things

# 1. FastAPI project
uvicorn app.main:app --reload

# 2. Celery worker in background.
celery -A app.tasks.tasks worker --loglevel=info

# 3. Unit Tests
python -m pytest tests/tests.py

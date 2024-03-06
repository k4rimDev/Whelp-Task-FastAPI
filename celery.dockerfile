FROM python:3.12

WORKDIR /code

ENV PYTHONPATH="${PYTHONPATH}:/code"

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["celery", "-A", "app.tasks.tasks", "worker", "--loglevel=info"]

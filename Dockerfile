# syntax=docker/dockerfile:1.2
FROM python:3.10
WORKDIR /app

COPY . .

RUN pip install uv
RUN uv pip install --system -r requirements.txt

EXPOSE 8080

CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:8080", "--timeout=0","--worker-class=uvicorn.workers.UvicornWorker", "server:app"]

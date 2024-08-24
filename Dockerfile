FROM python:3.11

WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY .env /app/.env

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY /api /app

EXPOSE 8080:8080

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
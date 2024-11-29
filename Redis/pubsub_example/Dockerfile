FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install redis

CMD ["python", "subscriber.py"]
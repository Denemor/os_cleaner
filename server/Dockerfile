FROM python:3.7-slim

WORKDIR /app

COPY . /app

RUN apt-get update && \
    apt-get install gcc -y && \
    pip install -r requirements.txt

CMD ["python", "manage.py"]

FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install django djangorestframework requests

CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000

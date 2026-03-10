FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install django djangorestframework requests

CMD python manage.py migrate --run-syncdb && python manage.py runserver 0.0.0.0:8000

# 1. Thêm pkg-config vào danh sách cài đặt của apt-get
RUN apt-get update && apt-get install -y pkg-config default-libmysqlclient-dev build-essential

# 2. Cài đặt các thư viện Python như bình thường
RUN pip install --upgrade pip
RUN pip install django djangorestframework requests mysqlclient
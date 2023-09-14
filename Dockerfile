FROM python:3.8 AS base
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


FROM base AS development
COPY requirements_dev.txt requirements_dev.txt
RUN pip install --no-cache-dir -r requirements_dev.txt
COPY . code
WORKDIR /code
EXPOSE 8000

#CMD ["sh","-c","python manage.py runserver 0.0.0.0:8000"]


FROM base AS production
COPY requirements_prod.txt requirements_prod.txt
RUN pip install --no-cache-dir -r requirements_prod.txt
COPY . code
WORKDIR /code
EXPOSE 8000


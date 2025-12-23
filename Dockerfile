FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencias del sistema 
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Variables GDAL
ENV GDAL_CONFIG=/usr/bin/gdal-config
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./app /app

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

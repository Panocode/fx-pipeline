FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# кеш
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# перенос проекта(копия)
COPY . .

# пайплайн
CMD ["python", "etl/scheduler.py"]
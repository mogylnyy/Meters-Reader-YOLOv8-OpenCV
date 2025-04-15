FROM python:3.10-slim

# Установка зависимостей системы (включая libgl1)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Установка зависимостей Python
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем весь проект
COPY . .

# Открываем порт
EXPOSE 5000

# Запуск приложения
CMD ["python", "main.py"]

FROM python:3.10-slim

WORKDIR /app

# 🔥 Install system dependencies (IMPORTANT)
RUN apt-get update && apt-get install -y \
    poppler-utils \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 📦 Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=200 -r requirements.txt
COPY . .

# 🚀 Expose port
EXPOSE 8000

# ▶️ Run app
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
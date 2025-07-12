FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# ✅ Install LibreOffice and required fonts
RUN apt-get update && \
    apt-get install -y \
        libreoffice \
        libreoffice-writer \
        fonts-dejavu-core \
        fonts-dejavu-extra \
        curl && \
    apt-get clean

# Create folders for file I/O
RUN mkdir -p /app/uploads /app/output

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

# ✅ Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Fix permissions for uploaded/converted files
RUN chmod -R 777 /app/uploads /app/output

EXPOSE 5000

CMD ["python", "app.py"]
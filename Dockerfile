FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y \
        libreoffice \
        libreoffice-writer \
        fonts-dejavu-core \
        fonts-dejavu-extra && \
    apt-get clean

WORKDIR /app
COPY . .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
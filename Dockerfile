FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system packages
RUN apt-get update && \
    apt-get install -y libreoffice curl && \
    apt-get clean

# Set work directory
WORKDIR /app

# Copy code
COPY . /app/

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Ensure folders exist
RUN mkdir -p uploads output && chmod -R 777 uploads output

EXPOSE 5000

CMD ["python", "app.py"]
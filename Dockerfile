# Use an official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install required packages
RUN apt-get update && \
    apt-get install -y libreoffice curl && \
    apt-get clean

# Set work directory
WORKDIR /app

# Copy app files
COPY . /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Create upload/output folders
RUN mkdir -p uploads output

# Expose port
EXPOSE 5000

# Run app
CMD ["python", "app.py"]

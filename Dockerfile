# Use the official Python image from the Docker Hub
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libc-dev \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get install -y redis-server

# Start Redis as a background service
CMD ["redis-server", "/etc/redis/redis.conf"]

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Install gunicorn
RUN pip install gunicorn

# Copy the entire project into the container
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Create superuser if not exists
RUN python manage.py createsu
# RUN python manage.py populate_users

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run the application with gunicorn
CMD ["gunicorn", "--workers=3", "leaderboard_project.wsgi:application", "--bind", "0.0.0.0:8080"]
CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]
CMD ["celery", "-A", "tasks", "beat", "--loglevel=info"]

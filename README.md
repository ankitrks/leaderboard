# Leaderboard API Project
This project is a Django-based REST API for managing a leaderboard. Users can gain or lose points, and the leaderboard updates and reorders based on these points. Additionally, the project includes scheduled tasks to identify the user with the highest points at regular intervals.

## Features
* User management: create, read, update, delete users
* Upload user photos to AWS S3
* Add or subtract points from users
* Automatic leaderboard updates and reordering
* Scheduled job to identify and store the highest scoring user every 5 minutes
* Swagger API documentation

## Requirements
* Docker
* Docker Compose
* Redis
* AWS S3

## Setup
### Environment Variables
Create a `.env` file in the root directory with the following content:

```
SECRET_KEY=<secret_key>
DEBUG=True
ALLOWED_HOSTS=*
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://redis:6379
AWS_ACCESS_KEY_ID=<aws_access_key_id>
AWS_SECRET_ACCESS_KEY=<aws_secret_access_key>
AWS_STORAGE_BUCKET_NAME=<s3_bucket_name>
AWS_S3_REGION_NAME=<s3_region>
```

### Docker
Ensure you have Docker and Docker Compose installed on the system.

### Installation
Clone the repository:
```
git clone https://github.com/ankitrks/leaderboard/
cd leaderboard-api
```

### Build and run the Docker containers:
```
docker-compose up --build
```

This will:

* Build the Docker images
* Start the database and Redis services
* Run migrations and populate the database with initial users
* Start the Django application and Celery workers

## Usage
### API Endpoints

The API documentation is available via Swagger. Once the application is running, navigate to:

http://localhost:8080/swagger/

### Management Commands
To populate the database with initial users, you can use the provided management command:

```
docker-compose exec backend python manage.py populate_users
```

### Scheduled Job
The scheduled job to identify the user with the highest points runs every 5 minutes. It stores the highest scoring user in the Winner table.

### Project Structure

```
leaderboard-api/
├── Dockerfile
├── docker-compose.yml
├── .env
├── .gitignore
├── README.md
├── leaderboard_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   ├── celery.py
│   ├── apps/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── tasks.py
│   │   ├── urls.py
│   │   ├── factories.py
│   │   └── management/
│   │       └── commands/
│   │           └── populate_users.py
│   ├── templates/
│   │   └── ...
│   ├── static/
│   │   └── ...
├── requirements.txt
└── manage.py
```

### Running Tests
To run the tests, use the following command:

```
docker-compose exec backend python manage.py test
```

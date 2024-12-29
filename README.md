# Advanced FastAPI Project v2

This is an advanced FastAPI project with a structure similar to Django, designed for scalability and maintainability. It allows users to create and manage their own apps dynamically.

## Setup

1. Clone the repository
2. Enter the repository path
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS and Linux: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Copy `.env.example` to `.env` and fill in your configuration details
7. Run migrations: `python manage.py migrate`

## Usage

Here are some commands you can use with `manage.py`:

- `python manage.py runserver`: Start the FastAPI development server
- `python manage.py createapp <app_name>`: Create a new app with the given name
- `python manage.py deleteapp <app_name>`: Delete an existing app
- `python manage.py listapps`: List all installed apps
- `python manage.py makemigrations`: Generate new database migrations
- `python manage.py migrate`: Apply database migrations
- `python manage.py test`: Run tests
- `python manage.py shell`: Start an interactive Python shell

## Project Structure

- `apps/`: Application modules (user-created)
- `core/`: Core functionality (config, database, security)
- `migrations/`: Database migration files
- `static/`: Static files
- `templates/`: HTML templates
- `tests/`: Global test files
- `utils/`: Utility functions and classes
- `main.py`: FastAPI application instance
- `manage.py`: Command-line interface for common tasks
- `wsgi.py`: WSGI server configuration for deployment

## Features

- Dynamic app creation and management
- Modular app structure for scalability
- Advanced configuration management using Pydantic
- Built-in user authentication and security features
- Automatic API documentation with Swagger UI
- Database migrations with Alembic
- CORS middleware configured
- Static file and template handling
- Deployment-ready with WSGI configuration

## Creating a New App

To create a new app, run:


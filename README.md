# RECursion NITD Website Backend

## Project Title

**RECursion NITD Website Backend**

## Functionalities

- User registration, login, and profile management
- Forum with questions, answers, and discussions
- Event creation, listing, updating, and details
- Interview experience sharing and browsing
- Blog content management
- Team member pages and team-related data
- Calendar-related event APIs
- Google social authentication
- Email notification support using SMTP
- REST API endpoints for frontend integration

## Tech Stack

- Python 3.11
- Django 3.2
- Django REST Framework
- Django Filters
- Django MarkdownX
- Django Prometheus
- social-auth-app-django
- dj-database-url
- python-decouple / python-dotenv

## Project Structure

- `requirements.txt` — project dependencies
- `website/` — Django application root
  - `manage.py` — Django management script
  - `website/` — project settings and URL configuration
    - `settings.py` — application settings
    - `urls.py` — root URL routing
    - `wsgi.py` — WSGI entrypoint
  - `blog/` — blog application
  - `events/` — event management application
  - `events_calendar/` — calendar API application
  - `forum/` — forum application
  - `getting_started/` — onboarding and guides app
  - `team/` — team management app
  - `user_profile/` — user profile and account app
  - `interview_exp/` — interview experience app
  - `utils/` — shared utilities

## Local Setup

### 1. Prerequisites

- Python 3.11
- pip
- Git
- Optional: Microsoft Visual C++ Build Tools if package compilation fails

### 2. Clone the repository

```powershell
cd C:\Users\hp\Downloads\RECursion_Website\RECursionNITD-website
```

### 3. Create a virtual environment

```powershell
python -m venv venv
```

### 4. Activate the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

If you are using Command Prompt:

```cmd
venv\Scripts\activate.bat
```

### 5. Install dependencies

```powershell
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

### 6. Add the database file

Place the downloaded database file here:

```text
website/db.sqlite3
```

### 7. Extract media files

Extract the downloaded `media.zip` into the `website/` folder.

### 8. Create `website/.env`

Create the env file and add the required configuration values. Do not commit secrets.

### 9. Apply database migrations

```powershell
cd website
python manage.py makemigrations
python manage.py migrate
```

### 10. Collect static files

```powershell
python manage.py collectstatic --noinput
```

### 11. Run the development server

```powershell
python manage.py runserver
```

Open the site at:

```text
http://127.0.0.1:8000/
```

## Contribution

- Create a separate branch for each change: `git checkout -b feature/your-change`
- Keep pull requests focused and small
- Add a clear title and description for each PR
- Include testing or setup steps in the PR description
- Request review from the team or maintainer

## Notes

- Environment variables should be stored in `website/.env` and kept private.
- If `DATABASE_URL` is not provided, the project defaults to SQLite at `website/db.sqlite3`.
- If using SQLite locally, database host/user/password settings are not required.
- The frontend repository is separate: `https://github.com/RECursion-NITD/RECursionNITD-Frontend`

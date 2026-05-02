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

#### Install Python 3.11

- Download Python 3.11 from the official website:  
  https://www.python.org/downloads/release/python-3110/
- *Windows (via winget)*: winget install -e --id Python.Python.3.11
- *macOS (via Homebrew)*: brew install python@3.11
- *Linux (Ubuntu/Debian)*: sudo apt update && sudo apt install python3.11 python3.11-venv


Verify Python version:

```python --version```

Expected output:

```Python 3.11.x```

### 2. Fork and Clone the Repository

- Go to:
  https://github.com/RECursion-NITD/RECursionNITD-website

- Click Fork to create your own copy

- Clone your fork:

```
git clone https://github.com/<your-username>/RECursionNITD-website.git
cd RECursionNITD-website

Add upstream remote:

git remote add upstream https://github.com/RECursion-NITD/RECursionNITD-website.git
git remote -v

Checkout development branch:

git checkout dev-api
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

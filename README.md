# RECursionNITD-website

Steps to Install

1. Create python virtualenv
2. Install all packages from requirements.txt
3. Create .env file in project root with dbdetails

Sample:
DB_NAME=HELLO_DJANGO
DB_USER=U_HELLO
DB_PASSWORD=hA8(scA@!fg3*sc&xaGh&6%-l<._&xCf
DB_HOST=127.0.0.1
DB_PORT=""

4. run python manage.py makemigrations
5. run python manage.py migrate
6. run python manage.py runserver

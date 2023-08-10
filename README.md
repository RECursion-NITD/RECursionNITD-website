# RECursionNITD-website

steps to install

1. create python virtualenv
2. install all packages from requirements.txt
3. create .env file in project root (website/) with dbdetails

sample:

```
DB_NAME=HELLO_DJANGO
DB_USER=U_HELLO
DB_PASSWORD=hA8(scA@!fg3*sc&xaGh&6%-l<._&xCf
DB_HOST=127.0.0.1
DB_PORT=""

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY='googlekey'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET='googleSECRET'
```

4. run ```python manage.py makemigrations```
5. run ```python manage.py migrate```
6. run ```python manage.py runserver```

POSTMAN API
COLLECTION: [REC DRF](https://postman.com/rec-drf-backend-00/workspace/recursion-drf-port-backend/api/3ccf67a5-e059-4d31-8d22-8f3302f94876/version/b021621d-8a18-4f86-aede-8e2737156e9c)
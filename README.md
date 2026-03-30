# REST_Project


 * Baza danych: SQLite
 * Dokumentacja API: Swagger
 * Interfejs użytkownika: Aplikacja webowa
 
## Install:

1. Create `.venv`
2. `pip install django djangorestframework`
3. `python manage.py migrate`: migracja DB


## Run: 
`python manage.py runserver`

## Check in browser:
* http://127.0.0.1:8000/api/users/
* Content:
```
{
  "email": "test@example.com",
  "name": "John Doe"
}```

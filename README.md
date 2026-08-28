# REST_Project


Celem projektu jest implementacja rozproszonego systemu aukcyjnego opartego o architekturę REST, umożliwiającego komunikację między frontendem i backendem poprzez API.


## Spis treści

1. Technologie
2. Funkcjonalności
3. Uruchomienie lokalne
4. Uruchomienie backendu przez Docker
5. Wdrożenie aplikacji w chmurze


## 1. Technologie

- Backend: Django REST Framework  
- Frontend: React  
- Baza danych: SQLite
- Dokumentacja API: 
  - Swagger (/api/docs/)
  - OpenAPI Schema (/api/schema/)
  - ReDoc (/api/redoc/)
  -  bardziej szczegółowa dokumentacja (np. ERD) znajduje się w folderze [docs](https://github.com/anahoreth1/REST_Project/tree/main/docs)
- Docker: używany do uruchamiania backendu
- Wdrożenie w chmurze:
  - backend: platforma Render ([link](https://render.com/))
  - frontend: GitHub Pages  


## 2. Funkcjonalności

- Rejestracja i logowanie użytkownika
- Tworzenie, pobieranie, edycja i usuwanie aukcji
- Filtrowanie aukcji po kategorii i statusie
- Składanie ofert na aukcje
- Automatyczne ustawianie statusu aukcji (`planned`, `active`, `ended`)
- Blokada składania ofert przed rozpoczęciem aukcji oraz po jej zakończeniu
- Walidacja danych (np. dla aukcji pole `start_date` musi być wcześniejsze niż `end_date`)
- Testy jednostkowe

Dodatkowe:
- Hasło nit jest widoczne (hash)
- Zaimplementowana autoryzacja JWT
- Model Bid chroni użytkownika
- Logowanie operacji (plik `logs` oraz console)
- Paginacja i filtrowanie wyników
- Sortowanie wyników

## 3. Uruchomienie lokalne

### 3.1. Backend

```bash
cd backend/auction_system
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Przykład backendu po uruchomieniu:

* Otwórz stronę http://127.0.0.1:8000/api/users/
* Do pola **Content** dodaj:

```json
{
  "email": "test@example.com",
  "name": "John Doe",
  "password": "12345678"
}
```
* Naciśnij przycisk "Post"


### 3.2. Frontend

Przed uruchomieniem frontendu lokalnie należy utworzyć plik `.env` w folderze `frontend` na podstawie pliku `.env.example`.

```
cd frontend
npm install
npm run dev
```

Przykład frontendu po uruchomieniu:
* Otwórz stronę http://localhost:5173/REST_Project/
* Sprawdź, czy frontend działa poprawnie


### 4. Uruchomienie backendu przez Docker

Uruchomienie backendu za pomocą Dockera stanowi dodatkową możliwość uruchomienia aplikacji w kontenerze.

```bash
cd backend/auction_system
docker build -t auction-backend .
docker run -p 8000:8000 auction-backend
```

Przykład backendu po uruchomieniu przez Docker:

* Otwórz stronę:
  http://127.0.0.1:8000/api/users/

* Do pola **Content** dodaj:

```json
{
  "email": "test@example.com",
  "name": "John Doe",
  "password": "12345678"
}
```
* Naciśnij przycisk "Post"


## 5. Wdrożenie aplikacji w chmurze

GitHub Actions realizuje automatyczne wdrażanie aplikacji (workflow jest dostępny tutaj: [link](https://github.com/anahoreth1/REST_Project/tree/main/.github/workflows)). 

Każdy commit do gałęzi `main` powoduje automatyczną aktualizację backendu i frontendu w chmurze.

* Frontend: https://anahoreth1.github.io/REST_Project/
* Backend (API): https://rest-project-backend.onrender.com/api/

Przykład działania backendu w chmurze:

* Otwórz stronę https://rest-project-backend.onrender.com/api/
* Do pola **Content** dodaj:

```json
{
  "email": "test@example.com",
  "name": "John Doe",
  "password": "12345678"
}
```

* Naciśnij przycisk ""POST".

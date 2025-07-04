# Semantic Analysis Tool

Narzędzie do analizy semantycznej odpowiedzi z ankiet w języku polskim i ukraińskim. Aplikacja umożliwia import danych z plików Excel, tagowanie odpowiedzi według kategorii semantycznych oraz analizę statystyczną wyników.

## 🚀 Funkcjonalności

- **Import danych** z plików Excel (.xlsx)
- **Filtrowanie odpowiedzi** według wartości, języka i typu
- **Tagowanie odpowiedzi** z kategoryzacją semantyczną
- **Edycja tagów** z możliwością zmiany kategorii
- **Eksport danych** do formatu CSV
- **Analiza statystyczna** z podsumowaniem tagów
- **Nowoczesny interfejs** z Tailwind CSS
- **Nawigacja z zachowaniem stanu** filtrów

## 🛠️ Wymagania systemowe

- Python 3.8+
- PostgreSQL
- Node.js (dla Tailwind CSS)

## 📦 Instalacja

### 1. Sklonuj repozytorium

```bash
git clone <repository-url>
cd analysis_tool
```

### 2. Utwórz wirtualne środowisko Python

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# lub
source venv/bin/activate  # Linux/Mac
```

### 3. Zainstaluj zależności

```bash
pip install -r requirements.txt
```

### 4. Skonfiguruj bazę danych PostgreSQL

Utwórz bazę danych PostgreSQL i użytkownika z odpowiednimi uprawnieniami.

### 5. Skonfiguruj zmienne środowiskowe

Utwórz plik `.env` w głównym katalogu projektu:

```bash
# Django settings
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database settings
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=5432
```

### 6. Wykonaj migracje bazy danych

```bash
python manage.py migrate
```

### 7. Zbuduj CSS z Tailwind

```bash
python manage.py tailwind install
python manage.py tailwind build
```

### 8. Zaimportuj dane z pliku Excel

```bash
python import_excel.py
```

### 9. Uruchom serwer deweloperski

```bash
python manage.py runserver
```

Aplikacja będzie dostępna pod adresem: http://127.0.0.1:8000/

## 📊 Struktura danych

### Modele Django

#### Answer (Odpowiedź)

- `value` - wartość (np. "MIŁOŚĆ", "WOLNOŚĆ")
- `language` - język ("pl" lub "ua")
- `type` - typ odpowiedzi ("skojarzenie" lub "definicja")
- `content` - treść odpowiedzi z ankiety

#### Tag (Tag)

- `name` - nazwa tagu
- `category` - kategoria semantyczna
- `value`, `language`, `type` - kontekst tagu

#### AnswerTag (Powiązanie)

- `answer` - powiązanie z odpowiedzią
- `tag` - powiązanie z tagiem

### Kategorie tagów

- **Określenie** (definition) - definicje i opisy
- **Obiekt** (object) - przedmioty i rzeczy
- **Pojęcie** (notion) - abstrakcyjne pojęcia
- **Doznanie** (experience) - doświadczenia i uczucia
- **Działanie** (action) - czynności i aktywności
- **Atrybut** (attributes) - cechy i właściwości

## 🔧 Użycie aplikacji

### 1. Lista odpowiedzi (`/answers/`)

- Przeglądanie wszystkich odpowiedzi
- Filtrowanie według wartości, języka i typu
- Sortowanie według ID
- Paginacja wyników

### 2. Szczegóły odpowiedzi (`/answers/<id>/`)

- Wyświetlanie pełnej treści odpowiedzi
- Dodawanie nowych tagów
- Przypisywanie istniejących tagów
- Usuwanie tagów

### 3. Edycja tagów (`/tag/<id>/edit/`)

- Zmiana nazwy tagu
- Zmiana kategorii tagu
- Powrót do poprzedniej strony

### 4. Analiza (`/analysis/`)

- Podsumowanie tagów według kategorii
- Statystyki użycia tagów

### 5. Eksport (`/export/`)

- Eksport wszystkich otagowanych odpowiedzi do CSV
- Format z kodowaniem UTF-8

## 📁 Struktura plików

```
analysis_tool/
├── analysis_tool/          # Główna konfiguracja Django
│   ├── settings.py         # Ustawienia projektu
│   ├── urls.py            # Główne URL-e
│   └── wsgi.py            # Konfiguracja WSGI
├── surveys/               # Główna aplikacja
│   ├── models.py          # Modele danych
│   ├── views.py           # Widoki
│   ├── forms.py           # Formularze
│   ├── urls.py            # URL-e aplikacji
│   ├── admin.py           # Panel administracyjny
│   ├── tests.py           # Testy
│   └── templates/         # Szablony HTML
├── theme/                 # Aplikacja Tailwind CSS
├── import_excel.py        # Skrypt importu danych
├── dane.xlsx             # Plik z danymi
├── manage.py             # Narzędzie zarządzania Django
├── requirements.txt      # Zależności Python
├── .env                  # Zmienne środowiskowe
└── .gitignore           # Pliki ignorowane przez Git
```

## 🧪 Testy

Uruchom testy jednostkowe:

```bash
python manage.py test
```

## 🔒 Bezpieczeństwo

- Wszystkie wrażliwe dane są przechowywane w zmiennych środowiskowych
- Plik `.env` jest ignorowany przez Git
- DEBUG jest kontrolowany przez zmienną środowiskową
- Hasła do bazy danych nie są w kodzie

## 🚀 Wdrażanie

### Produkcja

1. Ustaw `DJANGO_DEBUG=False` w zmiennych środowiskowych
2. Wygeneruj nowy `SECRET_KEY`
3. Skonfiguruj `ALLOWED_HOSTS` dla domeny produkcyjnej
4. Użyj serwera WSGI (np. Gunicorn)
5. Skonfiguruj serwer web (np. Nginx)

## 📝 Licencja

MIT License

## 👥 Autor

Alisa Borkowska

## 🤝 Współpraca

1. Fork projektu
2. Utwórz branch dla nowej funkcjonalności (`git checkout -b feature/AmazingFeature`)
3. Commit zmian (`git commit -m 'Add some AmazingFeature'`)
4. Push do branch (`git push origin feature/AmazingFeature`)
5. Otwórz Pull Request

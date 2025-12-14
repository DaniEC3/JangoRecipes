# JangoRecipes

A Django web app for browsing recipes, inspecting ingredients, and generating quick ingredient charts. Authenticated users can search, filter, and open detailed recipe pages that highlight nutrition and cost information.

## Features

- **Authentication** – Built-in login, logout, and registration flows protect the recipe catalog and redirect users back to the home page after successful sign-in.【F:jangorecipes/urls.py†L25-L34】【F:jangorecipes/view.py†L10-L56】
- **Recipe browsing** – The home page lists recipes in a grid with photos, cooking time, and difficulty labels, plus a quick link into the detail view.【F:recipes/templates/recipes/home.html†L6-L57】
- **Search** – Filter recipes by name using the search form; results update in-place without leaving the listing page.【F:recipes/views.py†L13-L65】【F:recipes/forms.py†L11-L12】
- **Rich recipe details** – Each recipe page shows the description, ingredients table, instructions, and per-ingredient metadata such as calories, price, and supplier, alongside the recipe image and difficulty badge.【F:recipes/templates/recipes/recipe_detail.html†L33-L110】【F:recipes/models.py†L7-L55】
- **Ingredient charts** – Select a chart type (price, calories, or quantity distribution) to render a Matplotlib graph directly on the recipe page.【F:recipes/templates/recipes/recipe_detail.html†L94-L105】【F:recipes/utils.py†L32-L86】

## Project structure

- `src/manage.py` – Django entry point for local commands.
- `src/jangorecipes/` – Project settings, URL routing, and authentication views.
- `src/recipes/` – Recipe app models, forms, utilities, and templates.
- `src/templates/` – Shared base layout.
- `src/staticfiles/` and `src/media/` – Collected static assets and uploaded recipe images.

## Getting started

### Prerequisites

- Python 3.12+
- `pip` for installing dependencies

### Installation

1. **Create and activate a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Database setup

Apply migrations to set up the SQLite database (stored at `src/db.sqlite3`):

```bash
python src/manage.py migrate
```

If you need an admin user for the Django admin or to sign in immediately, create one:

```bash
python src/manage.py createsuperuser
```

### Running the app locally

Start the development server from the project root:

```bash
python src/manage.py runserver
```

Then open `http://127.0.0.1:8000/` in your browser. Use the **Register** link to create an account or log in with existing credentials. Recipe images are served from `src/media/`, and collected static assets are in `src/staticfiles/`.

### Tests

Run the Django test suite:

```bash
python src/manage.py test
```

## Key URLs

- `/` – Recipe list with search and difficulty indicators.
- `/recipe/<id>` – Recipe detail page with ingredients, instructions, and charts.
- `/login`, `/logout`, `/register` – Authentication routes.

## Notes

- Static files are configured to collect into `STATIC_ROOT=src/staticfiles` (WhiteNoise is enabled for production).【F:jangorecipes/settings.py†L123-L133】
- Media uploads (recipe photos) are stored under `MEDIA_ROOT=src/media` and served via `/media/` during development.【F:jangorecipes/settings.py†L123-L133】

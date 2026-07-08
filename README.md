# TaskFlow

A modern, full-featured todo list web app built with Flask. Organize tasks with priorities, categories, due dates, and notes — all in a polished UI with dark mode support.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

- **Task management** — Add, edit, complete, and delete tasks
- **Priorities** — Low, Medium, High with color-coded badges
- **Categories** — General, Work, Personal, Shopping, Health
- **Due dates** — Overdue and "Due today" indicators
- **Notes** — Optional notes on each task
- **Search** — Find tasks by title or notes
- **Filters** — By status (All / Active / Completed) and category
- **Sorting** — Newest, oldest, priority, or due date
- **Stats dashboard** — Active, done, overdue, due today, completion progress
- **Bulk actions** — Mark all complete, clear completed tasks
- **Dark mode** — Toggle with preference saved in browser
- **Security** — CSRF protection on all forms

## Tech Stack

- **Backend:** Python 3, Flask 3, Flask-SQLAlchemy, Flask-WTF
- **Database:** SQLite
- **Frontend:** Custom HTML/CSS/JS (no Bootstrap or jQuery)

## Getting Started

### Prerequisites

- Python 3.10 or newer

### Installation

```bash
git clone https://github.com/YOUR_USERNAME/taskflow.git
cd taskflow

python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
python init_db.py
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

### Environment Variables (optional)

For production, set a secret key:

```bash
# Windows
set SECRET_KEY=your-secret-key-here

# macOS / Linux
export SECRET_KEY=your-secret-key-here
```

## Project Structure

```
├── app/
│   ├── __init__.py      # Flask app factory
│   ├── models.py        # Task model
│   ├── routes.py        # Route handlers
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/app.js
│   └── templates/
│       ├── base.html
│       └── index.html
├── app.py               # Entry point
├── config.py            # Configuration
├── init_db.py           # Database setup & migration
└── requirements.txt
```

## Database

The app uses SQLite. Run `python init_db.py` to create the database and apply schema migrations.

If upgrading from an older version, the migration script adds new columns automatically. To start fresh, delete the `instance/` folder and run `init_db.py` again.

## Deploying (live website from GitHub)

### GitHub Pages will NOT work

This is a **Python/Flask** app. GitHub Pages only hosts static HTML files — it cannot run Python or render Jinja templates. If you enable Pages, you'll see raw code like `{% extends "base.html" %}` and broken styling.

**Turn off GitHub Pages:** Repo → Settings → Pages → Source → **None**.

### Deploy with Render (free, connects to GitHub)

1. Push the latest code to GitHub (includes `render.yaml` and `gunicorn` in `requirements.txt`).
2. Go to [render.com](https://render.com) and sign up with GitHub.
3. Click **New +** → **Blueprint**.
4. Select your `To-Do-List` repository.
5. Render reads `render.yaml` and creates the web service automatically.
6. Click **Apply** — you'll get a live URL like `https://taskflow-xxxx.onrender.com`.

Every push to `main` auto-redeploys.

**Manual setup (if not using Blueprint):**

| Setting | Value |
|---------|-------|
| Build Command | `pip install -r requirements.txt && python init_db.py` |
| Start Command | `gunicorn app:app --bind 0.0.0.0:$PORT` |
| Environment | Add `SECRET_KEY` = any long random string |

> **Note:** On the free tier, SQLite data may reset when the app redeploys. Fine for demos; use PostgreSQL for production.

## Acknowledgments

This project is based on [Flask-ToDo-List](https://github.com/zacclery/Flask-ToDo-List) by Zac Clery, extended with a modern UI and additional features.

## License

MIT License — see [LICENSE](LICENSE) for details.

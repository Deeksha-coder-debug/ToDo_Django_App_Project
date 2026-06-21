# ✅ TaskMaster — Django To-Do App

A vibrant, interactive task management web application built with **Django**, featuring
priority-based task organization, due date tracking, and a modern colorful UI.

---

## Features

- ➕ **Add Tasks** — Create tasks with title, description, due date, and priority
- 🗑️ **Delete Tasks** — Remove tasks instantly with confirmation
- 🎯 **Set Priority** — Assign High, Medium, or Low priority to each task
- 📅 **Due Date Sorting** — Pending tasks sorted by nearest due date
- 🔴🟡🟢 **Priority Indicators** — Color-coded badges for quick visual scanning
- ⏰ **Overdue Alerts** — Highlights tasks past their due date
- ✅ **Mark Complete** — Toggle tasks between pending and completed
- 📊 **Task Summary** — Dashboard showing pending vs completed counts
- **Adds Category of Task** - Task is related to work,study or personal

---

## Tech Stack

- **Python**
- **Django**
- **SQLite** (default database)
- **HTML/CSS**
- **Bootstrap 5** (vibrant, responsive UI)
---

## Task Priority Levels

| Priority | Color | Badge |
|---|---|---|
| High | 🔴 Red | Urgent — do first |
| Medium | 🟡 Yellow | Normal tasks |
| Low | 🟢 Green | When time allows |

---

## Setup & Run

### 1. Clone the repo
```bash
git clone https://github.com/your-username/todo-django-app.git
cd todo-django-app
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the server
```bash
python manage.py runserver
```

### 6. Open in browser
```
http://127.0.0.1:8000/application
```

---

## How It Works

- Tasks are stored in **SQLite** via Django ORM
- Pending tasks are **sorted by due date** (earliest first), then by priority
- **Overdue tasks** are visually highlighted in red
- Priority is stored as a choice field: `High`, `Medium`, `Low`
- Completed tasks are moved to a separate section at the bottom

---

## Future Improvements

- 🔐 User authentication — personal task lists per user
- 🔔 Email/browser reminders for due tasks
- 🏷️ Task categories and tags
- 📱 Mobile-first responsive redesign
- 🔍 Search and filter functionality

---

## Author

Sai Deeksha Talabaktula

---

## Recent Fixes Walkthrough (June 2026)

Here is a summary of recent issues encountered in the `ToDo_Django_App_Project-main` codebase and how they were resolved to get the application running smoothly.

### 1. Authentication & Production Security Error
> [!WARNING]
> **Symptom:** CSRF validation failures and immediate logouts on the local environment.

**Root Cause:** The application was defaulting to `DEBUG = False`, activating production-grade security headers (`SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, and `CSRF_COOKIE_SECURE`). These policies actively reject cookies and forms sent over an unencrypted `http://localhost` connection.

**Resolution:**
- Created a `.env` file containing `DEBUG=True`.
- Imported the `python-dotenv` package in `todo_app/settings.py` to properly load the local environment variables.
- *Status: Login and sessions now function properly locally.*

### 2. Unapplied Database Migrations
> [!CAUTION]
> **Symptom:** `OperationalError: no such column: application_task.user_id` when viewing the dashboard.

**Root Cause:** The `Task` model in `application/models.py` had been updated to include a `user` foreign key and a `completed_at` field, but these structural changes were never synchronized with the `db.sqlite3` database.

**Resolution:**
- Ran `python manage.py makemigrations` to generate the schema blueprints.
- Ran `python manage.py migrate` to apply the missing columns to the database.
- *Status: The dashboard now loads without database crash errors.*

### 3. URL Namespace Resolution Errors
> [!IMPORTANT]
> **Symptom:** `NoReverseMatch: Reverse for 'index' not found` after submitting a form or clicking buttons.

**Root Cause:** The `application/urls.py` file defined a specific app namespace (`app_name = 'application'`). Because of this, Django requires all internal routing references to be explicitly prefixed with the namespace (e.g., `application:index`), but `views.py` and the templates were using the generic `'index'`.

**Resolution:**
- Updated all occurrences of `redirect('index')` to `redirect('application:index')` in `application/views.py` (Add, Edit, Complete, Delete actions).
- Updated the "Back to Task List" link in `add_task.html` to `{% url 'application:index' %}`.
- Removed deprecated/commented-out HTML blocks in `index.html` to prevent the Django template parser from tripping over broken `{% url %}` tags hidden inside HTML comments.
- *Status: All redirects and dashboard buttons navigate correctly.*

### 4. Timezone Misalignment & UI Typo
> [!NOTE]
> **Symptom:** Task completion times were off by 5.5 hours, and an extra `<` character appeared next to dates.

**Root Cause:** Django's `TIME_ZONE` was set to `UTC`, and there was a stray character in `index.html`.

**Resolution:**
- Updated `TIME_ZONE = 'Asia/Kolkata'` in `settings.py` so timestamps are stored and displayed in local Indian Standard Time.
- Removed the stray `<` character from the `task.completed_at` render block in `index.html`.
- *Status: The UI is completely clean and displays mathematically accurate local times.*

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


# FastAPI To-Do App with User Authentication ✅

A simple **FastAPI-based To-Do List App** with **JWT authentication**.
Users can **sign up, log in, and manage their personal tasks** (CRUD).
Built with **FastAPI + SQLAlchemy + JWT (python-jose) + SQLite** for quick dev setup.

---

## 🚀 Features

* 🔐 User Signup & Login (JWT-based authentication)
* 📝 CRUD operations for tasks (Create, Read, Update, Delete)
* 👤 Each user only sees their own tasks
* 🗄️ SQLite database (easy local dev, switch to PostgreSQL for production)
* ⚡ Interactive Swagger UI at `/docs`

---

## 📦 Installation

Clone this repo and install dependencies:

```bash
git clone https://github.com/azeemteli/fastapi-todo.git
cd fastapi-todo
```

Create and activate virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

Install requirements:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Inside `.env`:

```ini
SECRET_KEY="CHANGE_THIS_TO_A_RANDOM_SECRET_IN_PRODUCTION"
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL="sqlite:///./todo.db"
```

> 🔑 Generate a strong `SECRET_KEY` for production:
> `openssl rand -hex 32`

---

## ▶️ Run the App

```bash
uvicorn app.main:app --reload
```

Visit: **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)** for interactive API docs.

---

## 🧪 Example Usage

### 1. Sign Up

```bash
curl -X POST "http://127.0.0.1:8000/signup" \
 -H "Content-Type: application/json" \
 -d '{"email":"alice@example.com","password":"supersecret"}'
```

### 2. Login & Get Token

```bash
curl -X POST "http://127.0.0.1:8000/token" \
 -H "Content-Type: application/x-www-form-urlencoded" \
 -d "username=alice@example.com&password=supersecret"
```

Response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1...",
  "token_type": "bearer"
}
```

### 3. Create Task

```bash
curl -X POST "http://127.0.0.1:8000/tasks/" \
 -H "Authorization: Bearer YOUR_TOKEN_HERE" \
 -H "Content-Type: application/json" \
 -d '{"title":"Buy milk","description":"2 liters"}'
```

### 4. Get My Tasks

```bash
curl -X GET "http://127.0.0.1:8000/tasks/" \
 -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 📂 Project Structure

```
fastapi-todo/
├─ app/
│  ├─ __init__.py
│  ├─ main.py          # FastAPI routes
│  ├─ database.py      # DB setup
│  ├─ models.py        # SQLAlchemy models
│  ├─ schemas.py       # Pydantic schemas
│  ├─ crud.py          # CRUD logic
│  ├─ auth.py          # JWT utils + auth deps
│  └─ deps.py          # Shared dependencies (optional)
├─ requirements.txt
├─ .env.example
└─ README.md
```

---

## 🛠️ Tech Stack

* [FastAPI](https://fastapi.tiangolo.com/) 🚀
* [SQLAlchemy](https://www.sqlalchemy.org/) ORM
* [Passlib](https://passlib.readthedocs.io/) (bcrypt password hashing)
* [Python-Jose](https://python-jose.readthedocs.io/) (JWT auth)
* [Uvicorn](https://www.uvicorn.org/) ASGI server

---

## 📬 Newsletter & Source Code

👉 Get updates, more FastAPI projects, and **downloadable source code** here:
🔗 [https://azeemteli.gumroad.com/](https://azeemteli.gumroad.com/)

---

## ❤️ Support

If this project helped you:

* ⭐ Star the repo
* 👏 Clap the Medium article
* 📰 Subscribe to the newsletter

Your support keeps me building more open-source tutorials! 🚀

---

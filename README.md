
# FastAPI Expense Tracker API 💰

A simple **FastAPI-based Expense Tracking API** for managing user expenses.
Users can **add expenses and retrieve them by user ID** with optional category filtering.
Built with **FastAPI + Pydantic** for quick development and validation.

---

## 🚀 Features

* 💰 Add expenses for users
* 📊 Get all expenses or filter by user ID
* 🏷️ Filter expenses by category
* ✅ Data validation with Pydantic models
* ⚡ Interactive Swagger UI at `/docs`

---

## 📦 Installation

Clone this repo and install dependencies:

```bash
git clone https://github.com/utkarsh-0201/fastapi_project.git
cd fastapi_project
```

Create and activate virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

Install requirements:

```bash
pip install -r src/requirements.txt
```

---



---

## ▶️ Run the App

```bash
uvicorn src.main:app --reload
```

Visit: **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)** for interactive API docs.

---

## 🧪 Example Usage

### 1. Get All Expenses

```bash
curl -X GET "http://127.0.0.1:8000/"
```

### 2. Get User Expenses

```bash
curl -X GET "http://127.0.0.1:8000/expenses/123"
```

### 3. Get User Expenses by Category

```bash
curl -X GET "http://127.0.0.1:8000/expenses/123?category=food"
```

### 4. Add New Expense

```bash
curl -X POST "http://127.0.0.1:8000/expenses/123" \
 -H "Content-Type: application/json" \
 -d '{"amount":25.50,"category":"food","currency":"INR","vendor":"McDonald"}'
```

---

## 📂 Project Structure

```
fastapi_project/
├─ src/
│  ├─ main.py          # FastAPI app with expense routes
│  ├─ requirements.txt # Project dependencies
│  └─ README.md        # Additional documentation
├─ .gitignore
└─ README.md           # Main documentation
```

---

## 🛠️ Tech Stack

* [FastAPI](https://fastapi.tiangolo.com/) 🚀
* [Pydantic](https://pydantic-docs.helpmanual.io/) (data validation)
* [Uvicorn](https://www.uvicorn.org/) ASGI server

---

## 📋 API Endpoints

* `GET /` - Get all expenses for all users
* `GET /expenses/{user_id}` - Get expenses for a specific user
* `GET /expenses/{user_id}?category={category}` - Get expenses filtered by category
* `POST /expenses/{user_id}` - Add a new expense for a user

---

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_get_all_expenses():
    response = client.get("/")
    assert response.status_code == 200
    assert "123" in response.json()


def test_get_user_expenses():
    response = client.get("/expenses/123")
    assert response.status_code == 200
    assert len(response.json()) == 4


def test_get_user_expenses_by_category():
    response = client.get("/expenses/123?category=food")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_nonexistent_user():
    response = client.get("/expenses/999")
    assert response.status_code == 404


def test_add_expense():
    expense_data = {
        "amount": 50.0,
        "category": "food",
        "currency": "INR",
        "vendor": "Test Vendor"
    }
    response = client.post("/expenses/123", json=expense_data)
    assert response.status_code == 201
    assert response.json()["amount"] == 50.0
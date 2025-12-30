from types import SimpleNamespace

from fastapi.testclient import TestClient
from app.main import app
from app.core.dependencies import get_current_user


def override_current_user():
    return SimpleNamespace(user_id="test-user", email="test@example.com", is_active=True)


def test_get_all_expenses():
    app.dependency_overrides[get_current_user] = override_current_user
    client = TestClient(app)
    try:
        response = client.get("/expenses/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    finally:
        app.dependency_overrides.clear()

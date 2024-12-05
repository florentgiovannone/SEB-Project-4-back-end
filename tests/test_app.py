import pytest
from app import app 

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_hello(client):
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.data == b"Hello World!"

def test_login_route(client):
    response = client.post("/api/login", json={"username": "Testname", "password": "Testword123!"})

    assert response.status_code == 200
    assert "token" in response.get_json() 
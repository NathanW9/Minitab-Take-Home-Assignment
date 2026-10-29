import pytest
from app import app

#Create a test client
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_data(as_text=True) == "Minitab Service is Running!"

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}

def test_mean(client):
    response = client.post("/mean", json=[1, 2, 3, 4])
    assert response.status_code == 200
    assert response.get_data(as_text=True) == "2.5"

def test_stddev(client):
    response = client.post("/stddev", json=[1, 2, 3])
    assert response.status_code == 200
    assert response.get_data(as_text=True) == "0.816"

def test_rounding(client):
    response = client.post("/mean", json=[1.1111, 2])
    assert response.get_data(as_text=True) == "1.556"

def test_empty_array_input(client):
    response = client.post("/mean", json=[])
    assert response.status_code == 400

def test_boolean_input(client):
    response = client.post("/mean", json=[1, True, 3])
    assert response.status_code == 400
    assert response.json["error"] == "All values must be numbers"
    
def test_non_num_input(client):
    response = client.post("/stddev", json=["hello", 2])
    assert response.status_code == 400
    assert response.json["error"] == "All values must be numbers"

def test_non_array_input(client):
    response = client.post("/mean", json={"value": 5})
    assert response.status_code == 400

def test_malformed_input(client):
    response = client.post("/mean", data="[1, 2,", content_type="application/json")
    assert response.status_code == 400
    assert response.json["error"] == ("Must be an array of numbers")





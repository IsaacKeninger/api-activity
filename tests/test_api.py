from app import app
import pytest

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_hello(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {"message": "Hello World!"}

def test_square(client):
    response = client.get('/square/4')
    assert response.status_code == 200
    assert response.json == {"Area": 16,
                             "Shape": "Square"}

def test_echo(client):
    response = client.get('/echo?arg1=meta&arg2=sucks!')
    assert response.status_code == 200
    assert response.json == {"arg1": "meta",
                             "arg2": "sucks!"}
from api_activity.app import app, create_app
import pytest

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client

#Profile Endpoint Tests

def test_profile_requires_auth(client):
    response = client.get('/profile', base_url="https://localhost")
    assert response.status_code == 401

def test_profile_with_valid_auth(client):
    client.put(
        '/register',
        json={"username": "testuser", "password": "testpass123"},
        base_url="https://localhost",
    )

    response = client.get(
         "/profile",
         auth=("testuser", "testpass123"),
         base_url="https://localhost",
    )
    assert response.status_code == 200
    assert "testuser" in response.json["message"]

# Square Endpoint Tests

def test_square_requires_auth(client):
    response = client.get('/square/5', base_url="https://localhost")
    assert response.status_code == 401
    
def test_square(client):
    client.put(
        '/register',
        json={"username": "testuser", "password": "testpass123"},
        base_url="https://localhost",
    )
    response = client.get(
        '/square/5',
        auth=("testuser", "testpass123"),
        base_url="https://localhost",
    )
    assert response.status_code == 200
    assert response.json == {"Area": 25, "Shape": "Square"}

def test_square_zero(client):
    client.put(
        '/register',
        json={"username": "testuser", "password": "testpass123"},
        base_url="https://localhost",
    )
    response = client.get(
        '/square/0',
        auth=("testuser", "testpass123"),
        base_url="https://localhost",
    )
    assert response.status_code == 200
    assert response.json == {"message": "Square cannot have size of length 0."}

def test_square_negatives(client):
    client.put(
        '/register',
        json={"username": "testuser", "password": "testpass123"},
        base_url="https://localhost",
    )
    response = client.get(
        '/square/-1',
        auth=("testuser", "testpass123"),
        base_url="https://localhost",
    )
    assert response.status_code == 200
    assert response.json == {"message": "Square cannot have sides of negative integers."}

# Hello Endpoint Test

def test_hello(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {"message": "Hello World!"}

# Echo Endpoint Tests

def test_echo(client):
    response = client.get('/echo?arg1=meta&arg2=sucks!')
    assert response.status_code == 200
    assert response.json == {"arg1": "meta",
                             "arg2": "sucks!"}

def test_echo_no_args(client):
    response = client.get('/echo')
    assert response.status_code == 200
    assert response.json == {"arg1": None, "arg2": None}

def test_echo_only_arg1(client):
    response = client.get('/echo?arg1=foo')
    assert response.status_code == 200
    assert response.json == {"arg1": "foo", "arg2": None}

def test_echo_only_arg2(client):
    response = client.get('/echo?arg2=bar')
    assert response.status_code == 200
    assert response.json == {"arg1": None, "arg2": "bar"}

def test_echo_ignores_unknown_args(client):
    response = client.get('/echo?arg1=foo&arg3=ignored')
    assert response.status_code == 200
    assert response.json == {"arg1": "foo", "arg2": None}

def test_echo_wrong_method(client):
    response = client.post('/echo')
    assert response.status_code == 405
import jwt
import pytest
from fastapi.testclient import TestClient
from constants import ALGORITHM, SECRET_KEY
from database import TestSessionLocal, test_engine, Base
from main import app

# Fixture to set up the test database
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Set up - create all tables
    Base.metadata.create_all(bind=test_engine)
    pytest.MonkeyPatch().setenv('ENVIRONMENT', 'TESTING')

    # Run the tests
    yield
    
    # Teardown - drop all tables
    Base.metadata.drop_all(bind=test_engine)

# Fixture to provide a test database session
@pytest.fixture(scope="function")
def db_session():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


client = TestClient(app)


def test_register_success():
    """
    Test case for successful user registration.
    """
    # Define a user to register
    user_data = {"username": "TestUser1", "password": "Test@1234"}

    # Make a POST request to register the user
    with TestClient(app) as client:
        response = client.post("/register/", json=user_data)

    # Assert that the request was successful (status code 200)
    assert response.status_code == 200
    # Assert that the response body contains "Success"
    assert response.json() == "Success"


def test_register_failure():
    """
    Test case for successful user registration.
    """
    # Define a user to register
    user_data = {"username": "TestUser1", "password": "Test@1234"}

    # Make a POST request to register the user
    with TestClient(app) as client:
        response = client.post("/register/", json=user_data)

    # Assert that the request was successful (status code 200)
    assert response.status_code == 400


def test_register_validate_username():
    # Define a user to register
    user_data = {"username": "", "password": "Test@1234"}

    # Make a POST request to register the user
    with TestClient(app) as client:
        response = client.post("/register/", json=user_data)

    # Assert that the request was failed (status code 400)
    assert response.status_code == 400


def test_register_validate_password():
    # Define a user to register
    user_data = {"username": "TestUser2", "password": "Test"}

    # Make a POST request to register the user
    with TestClient(app) as client:
        response = client.post("/register/", json=user_data)

    # Assert that the request was failed (status code 400)
    assert response.status_code == 400

    user_data["password"] = "Test@"

    # Make a POST request to register the user
    with TestClient(app) as client:
        response = client.post("/register/", json=user_data)

    # Assert that the request was failed (status code 400)
    assert response.status_code == 400

    user_data["password"] = "test@1234"

    # Make a POST request to register the user
    with TestClient(app) as client:
        response = client.post("/register/", json=user_data)

    # Assert that the request was failed (status code 400)
    assert response.status_code == 400


def test_login_success():
    # Define a user to login
    user_data = {"username": "TestUser1", "password": "Test@1234"}

    # Make a POST request to login the user
    with TestClient(app) as client:
        response = client.post("/login/", json=user_data)

    # Assert that the request was successful (status code 200)
    assert response.status_code == 200

     # Decode the JWT access token and verify the username
    payload = jwt.decode(
        response.json().get("access_token"), SECRET_KEY, algorithms=[ALGORITHM]
    )
    assert user_data.get("username") == payload.get("name")


def test_login_failure():
    # Define invalid user credentials
    user_data = {"username": "TestUser1", "password": "Test@1231"}

    # Make a POST request to login the user
    with TestClient(app) as client:
        response = client.post("/login/", json=user_data)

    # Assert that the request failed with status code 401
    assert response.status_code == 401

    # Assert that the response contains the expected detail message
    assert response.json().get("detail") == "Invalid credentials"


def test_protected_api():
    # Define user credentials
    user_data = {"username": "TestUser1", "password": "Test@1234"}

    # Attempt to access the protected endpoint without authentication
    with TestClient(app) as client:
        response = client.get("/protected/")

    # Assert that the request without authentication fails with status code 403
    assert response.status_code == 403

    # Log in the user to obtain an access token
    with TestClient(app) as client:
        response = client.post("/login/", json=user_data)
    access_token = response.json().get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}

    # Access the protected endpoint with authentication
    with TestClient(app) as client:
        response = client.get("/protected/", headers=headers)

    # Assert that the request with authentication succeeds with status code 200
    assert response.status_code == 200

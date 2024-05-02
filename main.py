from datetime import datetime, timedelta
import jwt
import requests
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.security import HTTPBasic
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from constants import ALGORITHM, SECRET_KEY
from database import engine, get_db
from exceptions import validation_exception_handler
from map_my_crop.models import Base, User
from map_my_crop.schemas import (
    TokenSchema,
    UserSchema,
    WeatherRequestSchema,
    WeatherResponseSchema,
)
from utils import get_user, login_required

# Load environment variables from .env file
load_dotenv()

Base.metadata.create_all(bind=engine)

# Create the FastAPI instance
app = FastAPI()

# Register the exception handler for RequestValidationError
app.exception_handler(RequestValidationError)(validation_exception_handler)

# HTTP Basic authentication
security = HTTPBasic()

# Endpoint for user registration
@app.post("/register")
async def register(user: UserSchema, db: Session = Depends(get_db)):
    """
    Register a new user.

    Args:
        user (UserSchema): User information including username and password.

    Returns:
        str: Success message if registration is successful.
    """
    # Check if username already exists
    if get_user(user.username, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    # Hash the password
    user.password = bcrypt.hash(user.password)

    # Create a new user in the database
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return "Success"


# Endpoint for user authentication
@app.post("/login", response_model=TokenSchema)
async def login(credentials: UserSchema, db: Session = Depends(get_db)):
    """
    Log in an existing user.

    Args:
        credentials (UserSchema): User credentials including username and password.

    Returns:
        TokenSchema: JWT token if authentication is successful.
    """
    # Get user from database
    user = get_user(credentials.username, db)
    # Check if user exists and password is correct
    if not user or not bcrypt.verify(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    # Generate JWT token
    access_token = jwt.encode(
        {
            "name": user.username,
            "exp": datetime.utcnow() + timedelta(minutes=15)
        },
        key=SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return TokenSchema(access_token=access_token, token_type="bearer")


# # Protected endpoint requiring authentication
@app.get("/protected")
async def protected(user: dict = Depends(login_required)):
    """
    Protected endpoint that requires authentication.

    Args:
        user (dict): User information obtained from the JWT token.

    Returns:
        dict: A message indicating that the user is authenticated.
    """
    try:
        return {"message": f"{user.get('name')} is authenticated."}
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    

@app.post("/weather")
async def get_historic_weather(
            weather_request: WeatherRequestSchema,
            user: dict = Depends(login_required)
        ):
    """
    Retrieve historic weather data.

    Args:
        weather_request (WeatherRequestSchema): Request parameters including latitude,
            longitude, and number of days.
        user (dict): User information obtained from the JWT token.

    Returns:
        WeatherResponseSchema: Historic weather data for the specified location and time range.
    """
    # Make request to Open Meteo API using latitude, longitude, and number of days # noqa
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=weather_request.days)

    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={weather_request.latitude}&"
        f"longitude={weather_request.longitude}&"
        f"start_date={start_date.isoformat()}&"
        f"end_date={end_date.isoformat()}&"
        f"hourly=temperature_2m&hourly=precipitation&hourly=cloud_cover"
    )
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to retrieve weather data"
        )

    weather_data = response.json()

    # Process the response and extract weather data
    hourly_weather = weather_data.get("hourly", [])
    hourly_units = weather_data.get("hourly_units", {})

    # Return the weather data to the user
    return WeatherResponseSchema(
        latitude=weather_request.latitude,
        longitude=weather_request.longitude,
        days=weather_request.days,
        weather=hourly_weather,
        weather_units=hourly_units,
    )

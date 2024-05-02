import re

from pydantic import BaseModel, constr, Field, field_validator


# Pydantic model for user registration
class UserSchema(BaseModel):
    """
    Pydantic model for user registration.

    Attributes:
        username (str): The username of the user.
        password (str): The password of the user.

    Raises:
        ValueError: If username or password validation fails.
    """
    username: constr(min_length=1)
    password: constr(min_length=8)

    @field_validator("username")
    def validate_username(cls, username):
        """
        Validator for the username field.

        Args:
            username (str): The value of the username.

        Returns:
            str: The validated username.

        Raises:
            ValueError: If the username is empty or contains only whitespace.
        """
        # Check if the username is empty or contains only whitespace
        if not username.strip():
            raise ValueError("Username cannot be empty")
        return username

    @field_validator("password")
    def validate_password(cls, password):
        """
        Validator for the password field.

        Args:
            password (str): The value of the password.

        Returns:
            str: The validated password.

        Raises:
            ValueError: If the password does not meet the specified criteria.
        """

        # Minimum eight characters needed
        # At least one uppercase letter, one lowercase letter, one number, and one special character # noqa
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"  # noqa
        if not re.match(pattern, password):
            raise ValueError(
                "Password must contain at least 8 characters, one uppercase letter, one lowercase letter, one number, and one special character"  # noqa
            )
        return password


# Pydantic model for token response
class TokenSchema(BaseModel):
    """
    Pydantic model for token response.

    Attributes:
        access_token (str): The access token.
        token_type (str): The type of the token.

    Raises:
        ValueError: If access_token or token_type validation fails.
    """
    access_token: str
    token_type: str

    @field_validator("access_token", "token_type")
    def validate_fields(cls, v):
        """
        Validator for the access_token and token_type fields.

        Args:
            v (str): The value of the field.

        Returns:
            str: The validated value.

        Raises:
            ValueError: If the field is empty or contains only whitespace.
        """
        # Check if the field is empty or contains only whitespace
        if not v.strip():
            raise ValueError("Field cannot be empty")
        return v


class WeatherRequestSchema(BaseModel):
    """
    Pydantic model for weather request.

    Attributes:
        latitude (float): The latitude.
        longitude (float): The longitude.
        days (int): The number of days.

    Raises:
        ValueError: If latitude, longitude, or days validation fails.
    """
    latitude: float = Field(..., description="Latitude")
    longitude: float = Field(..., description="Longitude")
    days: int = Field(..., description="Number of days")


class WeatherResponseSchema(BaseModel):
    """
    Pydantic model for weather response.

    Attributes:
        latitude (float): The latitude.
        longitude (float): The longitude.
        days (int): The number of days.
        weather (dict): Weather data.
        weather_units (dict): Units of weather data.

    Raises:
        ValueError: If latitude, longitude, days, weather, or weather_units validation fails.
    """
    latitude: float = Field(..., description="Latitude")
    longitude: float = Field(..., description="Longitude")
    days: int = Field(..., description="Number of days")
    weather: dict = Field(..., description="Weather data")
    weather_units: dict = Field(..., description="Units of weather data")

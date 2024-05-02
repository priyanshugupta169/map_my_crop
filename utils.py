from datetime import datetime
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from constants import ALGORITHM, SECRET_KEY
from map_my_crop.models import User


# Decorator to check if the user is logged in
async def login_required(token: str = Depends(HTTPBearer())):
    """
    Check if the user is logged in by verifying the JWT token.

    Args:
        token (str): The JWT token passed as a Bearer token in the request header.

    Returns:
        dict: The payload of the JWT token if authentication is successful.

    Raises:
        HTTPException: If the token is invalid or expired, or if the user is not authenticated.
    """
    try:
        # Decode the JWT token and verify its authenticity
        payload = jwt.decode(
                        token.credentials,
                        SECRET_KEY,
                        algorithms=[ALGORITHM]
                    )
        
        # Extract the username from the payload
        username = payload.get("name")
        if not username:
            # If the username is not present in the payload, raise an authentication error
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        # Check if the token has expired
        exp = payload.get("exp")
        if exp is None or datetime.utcnow() > datetime.fromtimestamp(exp):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        # If authentication is successful, return the payload
        return payload
    except jwt.InvalidTokenError:
        # If the token is invalid, raise an authentication error
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


# Function to get user from database by username
def get_user(username: str, db: Session):
    """
    Retrieve user information from the database by username.

    Args:
        username (str): The username of the user to retrieve.
        db (Session): The SQLAlchemy database session.

    Returns:
        User: The user object if found, else None.
    """
    query = db.query(User)
    user_data = query.get(username)
    if user_data:
        return user_data
    else:
        return None

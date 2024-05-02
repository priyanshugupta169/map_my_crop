from sqlalchemy import Column, String

from database import Base


class User(Base):
    """
    SQLAlchemy model for user data.

    Attributes:
        username (str): The username of the user.
        password (str): The password of the user.

    """
    __tablename__ = "users"

    username = Column(String, primary_key=True, index=True)
    password = Column(String)

import os

# Secret key for JWT encoding and decoding
SECRET_KEY = os.getenv("SECRET_KEY", "test key")
ALGORITHM = "HS256"
DB_URL = "sqlite:///./map_my_crop.db"
TEST_DB_URL = "sqlite:///./test_map_my_crop.db"

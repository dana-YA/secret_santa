import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SWAGGER_SCHEME = os.getenv("SWAGGER_SCHEME", "http")
JWT_KEY = os.getenv("JWT_KEY")
# DB Settings
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

DB_URI = (
    os.getenv("DB_URL")
    or f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

DEBUG = os.getenv("DB_USER", False)

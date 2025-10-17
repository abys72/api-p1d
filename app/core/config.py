import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    JWT_EXPIRATION_SECONDS = os.environ.get("JWT_EXPIRATION_SECONDS")
    MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME")
    MONGO_ROOT_USER = os.environ.get("MONGO_ROOT_USER")
    MONGO_ROOT_PASSWORD = os.environ.get("MONGO_ROOT_PASSWORD")

    MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")

    MONGO_DB_URL = f"mongodb://{MONGO_ROOT_USER}:{MONGO_ROOT_PASSWORD}@{MONGO_HOST}:27017/"

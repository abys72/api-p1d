import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = "%IvD<HM/5TF73*Al.Ii#oo*^lyhG&Y_Zx|I8`*4zW~,"
    JWT_EXPIRATION_SECONDS = 3600
    MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME")
    MONGO_DB_URL = os.environ.get("MONGO_DB_URL")

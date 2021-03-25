import os

PROJECT_NAME = "vocable_me"

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or 'postgresql://postgres:password@postgres:5432/postgres'

API_V1_STR = "/api/v1"

# config.py
import os
from datetime import timedelta


# ----------------------------
# SECURITY
# ----------------------------

# NOTE:
# In testing, set this as an environment variable.

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "CHANGE_IN_FUTURE")

JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# ----------------------------
# DATABASE
# ----------------------------

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:password@localhost:5432/revision_optimizer"
)


# ----------------------------
# APPLICATION
# ----------------------------

APP_NAME = "Revision Optimizer"
APP_VERSION = "1.0.0"

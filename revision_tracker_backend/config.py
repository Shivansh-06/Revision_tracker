# config.py
import os
from datetime import timedelta


# ----------------------------
# SECURITY
# ----------------------------

# NOTE:
# In production, set this as an environment variable.
# Example:
# export JWT_SECRET_KEY="super-random-secret"
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "CHANGE_ME_IN_PRODUCTION")

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

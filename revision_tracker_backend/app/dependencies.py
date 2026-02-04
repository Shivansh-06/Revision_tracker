# app/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from jose import JWTError

from app.db import get_async_session
from app.jwt import decode_access_token
from app import models

http_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_scheme),
    session: AsyncSession = Depends(get_async_session),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    token = credentials.credentials

    try:
        payload = decode_access_token(token)
        print("JWT PAYLOAD:", payload)

        user_id_str = payload.get("sub")
        if not user_id_str:
            raise credentials_exception

        user_id = UUID(user_id_str)

    except JWTError as e:
        print("JWT ERROR:", repr(e))
        raise credentials_exception

    except Exception as e:
        print("AUTH ERROR:", repr(e))
        raise credentials_exception

    result = await session.execute(
        select(models.User).where(models.User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user

# app/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.db import get_async_session
from app import models
from app.schemas import UserCreate, UserRead
from app.security import hash_password, verify_password
from app.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead)
async def register_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        # Check if email already exists
        result = await session.execute(
            select(models.User).where(models.User.email == user_in.email)
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        user = models.User(
            email=user_in.email,
            hashed_password=hash_password(user_in.password),
        )

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user
    except HTTPException:
        raise
    except Exception as e:
        print(f"Registration error: {repr(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )

@router.post("/login")
async def login_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        result = await session.execute(
            select(models.User).where(models.User.email == user_in.email)
        )
        user = result.scalar_one_or_none()

        if not user or not verify_password(
            user_in.password,
            user.hashed_password,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        access_token = create_access_token(
            {"sub": str(user.id)}
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {repr(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )

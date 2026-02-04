from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, distinct
from app.db import get_async_session
from app.dependencies import get_current_user
from app import models

router = APIRouter(prefix="/subjects", tags=["subjects"])

@router.get("/")
async def list_subjects(
    session: AsyncSession = Depends(get_async_session),
    user=Depends(get_current_user),
):
    stmt = (
        select(distinct(models.Topic.subject))
        .where(models.Topic.user_id == user.id)
    )

    result = await session.execute(stmt)
    subjects = [row[0] for row in result.all()]

    return {
        "count": len(subjects),
        "subjects": subjects
    }

@router.get("/{subject}/units")
async def list_units(
    subject: str,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(get_current_user),
):
    stmt = (
        select(distinct(models.Topic.unit))
        .where(
            models.Topic.user_id == user.id,
            models.Topic.subject == subject,
        )
    )

    result = await session.execute(stmt)
    units = [row[0] for row in result.all()]

    return {
        "subject": subject,
        "units": units
    }

@router.get("/{subject}/units/{unit}/topics")
async def list_topics(
    subject: str,
    unit: str,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(get_current_user),
):
    stmt = (
        select(models.Topic)
        .where(
            models.Topic.user_id == user.id,
            models.Topic.subject == subject,
            models.Topic.unit == unit,
        )
    )

    result = await session.execute(stmt)
    topics = result.scalars().all()

    return [
        {
            "id": t.id,
            "name": t.name,
            "difficulty": t.difficulty,
            "importance": t.importance,
            "last_revised": t.last_revised,
        }
        for t in topics
    ]

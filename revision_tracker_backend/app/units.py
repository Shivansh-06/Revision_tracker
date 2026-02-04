from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, distinct
from app.db import get_async_session
from app.dependencies import get_current_user
from app import models
from sqlalchemy import delete, update
from pydantic import BaseModel

router = APIRouter(prefix="/units", tags=["units"])

@router.get("/")
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
        "count": len(units),
        "units": units
    }

@router.get("/{unit}/topics")
async def list_unit_topics(
    unit: str,
    subject: str,
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


@router.delete("/{unit}")
async def delete_unit(
    unit: str,
    subject: str,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(get_current_user),
):
    stmt = (
        delete(models.Topic)
        .where(
            models.Topic.user_id == user.id,
            models.Topic.subject == subject,
            models.Topic.unit == unit,
        )
    )

    result = await session.execute(stmt)
    await session.commit()

    return {
        "deleted": result.rowcount,
        "unit": unit,
        "subject": subject,
    }

class UnitRenameRequest(BaseModel):
    new_unit: str


@router.patch("/{unit}/rename")
async def rename_unit(
    unit: str,
    payload: UnitRenameRequest,
    subject: str,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(get_current_user),
):
    stmt = (
        update(models.Topic)
        .where(
            models.Topic.user_id == user.id,
            models.Topic.subject == subject,
            models.Topic.unit == unit,
        )
        .values(unit=payload.new_unit)
    )

    result = await session.execute(stmt)
    await session.commit()

    return {
        "updated": result.rowcount,
        "old_unit": unit,
        "new_unit": payload.new_unit,
    }
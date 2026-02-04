# app/topics.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import get_async_session
from app.dependencies import get_current_user
from app import app, models
from app.schemas import TopicBulkCreate, TopicCreate, TopicRead




router = APIRouter(prefix="/topics", tags=["topics"])

@router.post("/", response_model=TopicRead)
async def create_topic(
    topic_in: TopicCreate,
    session: AsyncSession = Depends(get_async_session),
    user: models.User = Depends(get_current_user),
):
    topic = models.Topic(
        user_id=user.id,
        subject=topic_in.subject,
        unit=topic_in.unit,
        name=topic_in.name,
        difficulty=topic_in.difficulty,
        importance=topic_in.importance,
    )

    session.add(topic)
    await session.commit()
    await session.refresh(topic)

    return topic

@router.get("/", response_model=list[TopicRead])
async def get_topics(
    session: AsyncSession = Depends(get_async_session),
    user: models.User = Depends(get_current_user),
):
    result = await session.execute(
        select(models.Topic).where(models.Topic.user_id == user.id)
    )
    return result.scalars().all()


@router.post("/bulk")
async def bulk_create_topics(
    topics: list[TopicBulkCreate],
    session: AsyncSession = Depends(get_async_session),
    user=Depends(get_current_user),
):
    objects = []

    for topic in topics:
        obj = models.Topic(
            user_id=user.id,
            subject=topic.subject,
            unit=topic.unit,
            name=topic.name,
            difficulty=topic.difficulty,
            importance=topic.importance,
        )
        objects.append(obj)

    session.add_all(objects)
    await session.commit()

    return {
        "created": len(objects)
    }

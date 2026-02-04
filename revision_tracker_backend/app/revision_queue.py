# app/revision_queue.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import aliased
from app.models import Topic, Revision

from app.db import get_async_session
from app.dependencies import get_current_user
from app import models
from app.revision_logic import compute_priority

router = APIRouter(prefix="/revision-queue", tags=["revision"])

@router.get("/")
async def get_revision_queue(
    session: AsyncSession = Depends(get_async_session),
    current_user: models.User = Depends(get_current_user)
):
    stmt = select(models.Topic).where(models.Topic.user_id == current_user.id)
    result = await session.execute(stmt)
    topics = result.scalars().all()

    response = []

    for topic in topics:
        priority = compute_priority(topic, current_user.priority_mode)

        response.append({
            "id": topic.id,
            "subject": topic.subject,
            "unit": topic.unit,
            "name": topic.name,
            "priority": priority,
            "last_revised": topic.last_revised,
        })

    response.sort(key=lambda t: t["priority"], reverse=True)
    return response

def bucket_from_priority(p: float) -> str:
    if p >= 0.75:
        return "overdue"
    elif p >= 0.4:
        return "due"
    else:
        return "fresh"
    
def compute_unit_progress(unit_buckets: dict) -> dict:
    overdue = len(unit_buckets["overdue"])
    due = len(unit_buckets["due"])
    fresh = len(unit_buckets["fresh"])

    total = overdue + due + fresh
    progress = (fresh / total) if total > 0 else 0.0

    return {
        "total": total,
        "overdue": overdue,
        "due": due,
        "fresh": fresh,
        "progress": round(progress, 2)
    }

def compute_subject_progress(units: dict) -> dict:
    total = overdue = due = fresh = 0

    for unit_data in units.values():
        p = unit_data["progress"]
        total += p["total"]
        overdue += p["overdue"]
        due += p["due"]
        fresh += p["fresh"]

    progress = (fresh / total) if total > 0 else 0.0

    return {
        "total": total,
        "overdue": overdue,
        "due": due,
        "fresh": fresh,
        "progress": round(progress, 2)
    }



@router.get("/unit-wise")
async def unit_wise_revision_queue(
    session: AsyncSession = Depends(get_async_session),
    user=Depends(get_current_user),
):
    stmt = (
        select(models.Topic)
        .where(models.Topic.user_id == user.id)
    )

    result = await session.execute(stmt)
    topics = result.scalars().all()

    queue = {}

    for topic in topics:
        priority = compute_priority(topic)

        subject = topic.subject
        unit = topic.unit
        bucket = bucket_from_priority(priority)

        queue.setdefault(subject, {})
        queue[subject].setdefault(unit, {
            "buckets":{
                "overdue": [],
                "due": [],
                "fresh": []
            },
            "progress": {}
        })

        queue[subject][unit]["buckets"][bucket].append({
            "id": topic.id,
            "name": topic.name,
            "priority": priority,
            "difficulty": topic.difficulty,
            "importance": topic.importance,
            "last_revised": topic.last_revised,
        })

    # Sort topics INSIDE each bucket
    for subject in queue:
        for unit in queue[subject]:
            unit_data = queue[subject][unit]
            buckets = unit_data["buckets"]

            for bucket_name, topics in buckets.items():
                topics.sort(
                    key=lambda t: t["priority"],
                    reverse=True
                )
            unit_data["progress"] = compute_unit_progress(buckets)
    for subject in queue:
        subject_units = {
            k: v for k, v in queue[subject].items()
            if not k.startswith("_")
        }

        queue[subject]["_meta"] = compute_subject_progress(subject_units)



    return queue

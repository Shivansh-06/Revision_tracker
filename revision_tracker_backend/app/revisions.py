from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.db import get_async_session
from app.dependencies import get_current_user
from app import models
from app.schemas import RevisionCreate
from app.revision_logic import priority_modes, compute_priority
from datetime import datetime, timedelta, timezone

DAILY_REVISION_GOAL = 5
NEGLECT_WEIGHT = 10.0


router = APIRouter(prefix="/revisions", tags=["revisions"])

class PriorityModeRequest(BaseModel):
    mode: str

@router.post("/")
async def add_revision(
    revision_in: RevisionCreate,
    session: AsyncSession = Depends(get_async_session),
    user: models.User = Depends(get_current_user),
):
    # Ensure topic belongs to user
    result = await session.execute(
        select(models.Topic).where(
            models.Topic.id == revision_in.topic_id,
            models.Topic.user_id == user.id
        )
    )
    topic = result.scalar_one_or_none()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    revision = models.Revision(
        topic_id=topic.id,
        confidence=revision_in.confidence,
    )

    topic.last_revised = datetime.now(timezone.utc)

    session.add(revision)
    await session.commit()

    return {"success": True}

@router.post("/{topic_id}/mark")
async def mark_topic_revised(
    topic_id: str,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(get_current_user),
):
    stmt = (
        select(models.Topic)
        .where(
            models.Topic.id == topic_id,
            models.Topic.user_id == user.id,
        )
    )

    result = await session.execute(stmt)
    topic = result.scalar_one_or_none()

    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    topic.last_revised = datetime.now(timezone.utc)

    # Optional: track revision count
    if hasattr(topic, "times_revised") and topic.times_revised is not None:
        topic.times_revised += 1

    await session.commit()

    return {
        "id": topic.id,
        "name": topic.name,
        "last_revised": topic.last_revised,
    }

@router.post("/unit/{unit}/mark")
async def mark_unit_revised(
    unit: str,
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
        .values(last_revised=datetime.now(timezone.utc))
    )

    result = await session.execute(stmt)
    await session.commit()

    if result.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="No topics found for this unit",
        )

    return {
        "subject": subject,
        "unit": unit,
        "updated_topics": result.rowcount,
        "last_revised": datetime.utcnow(),
    }

def is_today(dt: datetime) -> bool:
    if not dt:
        return False

    now = datetime.now(timezone.utc)
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    return dt >= start_of_day

@router.get("/daily-goal")
async def daily_revision_goal(
    session: AsyncSession = Depends(get_async_session),
    user=Depends(get_current_user),
):
    stmt = (
        select(models.Topic.last_revised)
        .where(
            models.Topic.user_id == user.id,
            models.Topic.last_revised.isnot(None),
        )
    )

    result = await session.execute(stmt)
    revised_dates = result.scalars().all()

    revised_today = sum(
        1 for dt in revised_dates if is_today(dt)
    )

    progress = min(revised_today / DAILY_REVISION_GOAL, 1.0)

    return {
        "goal": DAILY_REVISION_GOAL,
        "revised_today": revised_today,
        "remaining": max(DAILY_REVISION_GOAL - revised_today, 0),
        "progress": round(progress, 2),
        "completed": revised_today >= DAILY_REVISION_GOAL,
    }

def start_of_day(dt: datetime) -> datetime:
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)

@router.get("/weekly-summary")
async def weekly_summary(
    session: AsyncSession = Depends(get_async_session),
    user=Depends(get_current_user),
):
    now = datetime.now(timezone.utc)
    start = start_of_day(now - timedelta(days=6))

    stmt = (
        select(models.Topic.last_revised)
        .where(
            models.Topic.user_id == user.id,
            models.Topic.last_revised.isnot(None),
            models.Topic.last_revised >= start,
        )
    )

    result = await session.execute(stmt)
    revisions = result.scalars().all()

    # Initialize last 7 days
    days = {}
    for i in range(7):
        day = start_of_day(start + timedelta(days=i))
        days[day.date().isoformat()] = 0

    # Count revisions per day
    for dt in revisions:
        day_key = start_of_day(dt).date().isoformat()
        if day_key in days:
            days[day_key] += 1

    total = sum(days.values())
    average = round(total / 7, 2)

    return {
        "total_revised": total,
        "average_per_day": average,
        "days": days
    }


@router.get("/weekly-summary/subject")
async def subject_wise_weekly_summary(
    session: AsyncSession = Depends(get_async_session),
    user=Depends(get_current_user),
):
    now = datetime.now(timezone.utc)
    start = start_of_day(now - timedelta(days=6))

    stmt = (
        select(models.Topic.subject, models.Topic.last_revised)
        .where(
            models.Topic.user_id == user.id,
            models.Topic.last_revised.isnot(None),
            models.Topic.last_revised >= start,
        )
    )

    result = await session.execute(stmt)
    rows = result.all()

    # Prepare last 7 days template
    days_template = {}
    for i in range(7):
        day = start_of_day(start + timedelta(days=i))
        days_template[day.date().isoformat()] = 0

    summary = {}

    for subject, revised_at in rows:
        if subject not in summary:
            summary[subject] = {
                "days": days_template.copy(),
                "total": 0,
                "average_per_day": 0.0,
            }

        day_key = start_of_day(revised_at).date().isoformat()
        if day_key in summary[subject]["days"]:
            summary[subject]["days"][day_key] += 1
            summary[subject]["total"] += 1

    # Compute averages
    for subject in summary:
        summary[subject]["average_per_day"] = round(
            summary[subject]["total"] / 7, 2
        )

    return summary

@router.get("/subject-balance")
async def subject_balance_suggestions(
    session: AsyncSession = Depends(get_async_session),
    user=Depends(get_current_user),
):
    now = datetime.now(timezone.utc)
    start = start_of_day(now - timedelta(days=6))

    stmt = (
        select(models.Topic.subject, models.Topic.last_revised)
        .where(
            models.Topic.user_id == user.id,
            models.Topic.last_revised.isnot(None),
            models.Topic.last_revised >= start,
        )
    )

    result = await session.execute(stmt)
    rows = result.all()

    # Count revisions per subject
    subject_counts = {}
    total_revisions = 0

    for subject, _ in rows:
        subject_counts[subject] = subject_counts.get(subject, 0) + 1
        total_revisions += 1

    if total_revisions == 0:
        return {
            "message": "No revisions yet this week",
            "suggestions": []
        }

    num_subjects = len(subject_counts)
    expected_share = 1 / num_subjects

    suggestions = []

    for subject, count in subject_counts.items():
        actual_share = count / total_revisions

        if actual_share < expected_share * 0.75:
            status = "under-revised"
            suggestion = f"Focus more on {subject}"
        elif actual_share > expected_share * 1.25:
            status = "over-focused"
            suggestion = f"You may be over-focusing on {subject}"
        else:
            status = "balanced"
            suggestion = f"{subject} is well balanced"

        suggestions.append({
            "subject": subject,
            "revised_this_week": count,
            "share": round(actual_share, 2),
            "status": status,
            "suggestion": suggestion,
        })

    return {
        "total_revisions": total_revisions,
        "expected_share": round(expected_share, 2),
        "subjects": suggestions,
    }

@router.get("/daily-goal/subject")
async def adaptive_daily_goal_per_subject(
    session: AsyncSession = Depends(get_async_session),
    user=Depends(get_current_user),
):
    # 1) Build subject -> backlog from current buckets
    # Reuse your unit-wise queue builder logic OR query directly
    stmt = select(
        models.Topic.subject,
        models.Topic.last_revised
    ).where(models.Topic.user_id == user.id)

    rows = (await session.execute(stmt)).all()

    # Count backlog by subject using priority buckets
    backlog = {}  # subject -> {overdue, due}
    for subject, last_revised in rows:
        # compute priority the same way you do in the queue
        topic = models.Topic(subject=subject, last_revised=last_revised)
        p = compute_priority(topic)

        bucket = "fresh"
        if p >= 0.75:
            bucket = "overdue"
        elif p >= 0.4:
            bucket = "due"

        backlog.setdefault(subject, {"overdue": 0, "due": 0})
        if bucket in ("overdue", "due"):
            backlog[subject][bucket] += 1

    # 2) Weekly shares (reuse logic from subject-wise weekly summary)
    now = datetime.now(timezone.utc)
    start = (now - timedelta(days=6)).replace(hour=0, minute=0, second=0, microsecond=0)

    stmt2 = (
        select(models.Topic.subject)
        .where(
            models.Topic.user_id == user.id,
            models.Topic.last_revised.isnot(None),
            models.Topic.last_revised >= start,
        )
    )
    subjects_week = [r[0] for r in (await session.execute(stmt2)).all()]

    total_week = len(subjects_week)
    weekly_counts = {}
    for s in subjects_week:
        weekly_counts[s] = weekly_counts.get(s, 0) + 1

    subjects = set(list(backlog.keys()) + list(weekly_counts.keys()))
    if not subjects:
        return {"message": "No subjects yet", "goals": []}

    expected_share = 1 / len(subjects)

    # 3) Compute raw scores
    raw_scores = {}
    for s in subjects:
        overdue = backlog.get(s, {}).get("overdue", 0)
        due = backlog.get(s, {}).get("due", 0)
        urgency = overdue + 0.5 * due

        actual_share = (weekly_counts.get(s, 0) / total_week) if total_week else 0
        neglect = max(0.0, expected_share - actual_share)

        raw_scores[s] = urgency + NEGLECT_WEIGHT * neglect

    total_score = sum(raw_scores.values()) or 1.0

    # 4) Allocate today’s goal proportionally
    goals = []
    for s, score in raw_scores.items():
        allocated = max(1, round(DAILY_REVISION_GOAL * (score / total_score)))
        goals.append({
            "subject": s,
            "today_goal": allocated,
            "overdue": backlog.get(s, {}).get("overdue", 0),
            "due": backlog.get(s, {}).get("due", 0),
            "reason": "urgency + neglect",
        })

    return {
        "base_daily_goal": DAILY_REVISION_GOAL,
        "subjects": goals
    }

@router.get("/streak")
async def revision_streak(
    session: AsyncSession = Depends(get_async_session),
    user=Depends(get_current_user),
):
    # Fetch all revision dates
    stmt = (
        select(models.Topic.last_revised)
        .where(
            models.Topic.user_id == user.id,
            models.Topic.last_revised.isnot(None),
        )
    )

    result = await session.execute(stmt)
    dates = result.scalars().all()

    if not dates:
        return {
            "current_streak": 0,
            "longest_streak": 0,
            "active_today": False,
        }

    # Normalize to unique days
    revised_days = sorted({
        start_of_day(dt).date()
        for dt in dates
    })

    today = datetime.now(timezone.utc).date()

    if today in revised_days:
        current_streak = 0
        day = today
        revised_set = set(revised_days)

        while day in revised_set:
            current_streak += 1
            day -= timedelta(days=1)
        active_today = True
    else:
        current_streak = 0
        active_today = False

        # ---- LONGEST STREAK ----
    longest_streak = 1
    streak = 1

    for i in range(1, len(revised_days)):
        if revised_days[i] == revised_days[i - 1] + timedelta(days=1):
            streak += 1
            longest_streak = max(longest_streak, streak)
        else:
            streak = 1

    return {
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "active_today": active_today,
    }

@router.get("/priority-modes")
async def list_priority_modes():
    return {
        "modes": list(priority_modes.keys())
    }


@router.post("/priority-mode")
async def set_priority_mode(
    payload: PriorityModeRequest,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(get_current_user),
):
    if payload.mode not in priority_modes:
        raise HTTPException(400, "Invalid priority mode")

    user.priority_mode = payload.mode
    await session.commit()

    return {
        "priority_mode": user.priority_mode
    }
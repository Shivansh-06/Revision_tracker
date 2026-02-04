import math
from datetime import datetime, timezone
from typing import Literal

priority_modes = {
    "balanced": {"time": 0.55, "difficulty": 0.25, "importance": 0.20},
    "exam": {"time": 0.40, "difficulty": 0.30, "importance": 0.30},
    "revision": {"time": 0.70, "difficulty": 0.20, "importance": 0.10},
}


def estimate_stability(topic):
    base = 8
    difficulty_factor = 6 - topic.difficulty   # hard topic → low stability
    importance_factor = 1 + (topic.importance / 5)
    return max(base * difficulty_factor * importance_factor, 1)


def estimate_retrievability(topic):
    if not topic.last_revised:
        return 0.0
    days = (datetime.now(timezone.utc) - topic.last_revised).days
    stability = estimate_stability(topic)
    return math.exp(-days / stability)


def compute_priority(topic, mode: Literal["balanced", "exam", "revision"] = "balanced") -> float:
    weights = priority_modes.get(mode, priority_modes["balanced"])

    retrievability = estimate_retrievability(topic)
    forgetting_risk = 1 - retrievability  # 0 → remembered, 1 → forgotten

    difficulty_factor = topic.difficulty / 5
    importance_factor = topic.importance / 5

    priority = (
        weights["time"] * forgetting_risk +
        weights["difficulty"] * difficulty_factor +
        weights["importance"] * importance_factor
    )

    return round(priority, 4)

def build_revision_queue(topics, limit=15, mode="balanced"):
    scored = [(compute_priority(t, mode), t) for t in topics]
    scored.sort(key=lambda x: x[0], reverse=True)

    return [t for _, t in scored[:limit]]


def should_revise(topic):
    if not topic.last_revised:
        return True
    days = (datetime.now(timezone.utc) - topic.last_revised).days
    return days >= 1  # at least 1 day gap

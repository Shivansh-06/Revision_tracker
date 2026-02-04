import re
from typing import Dict, List, Optional

MAX_TOPIC_LENGTH = 120


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def looks_like_unit(line: str) -> bool:
    return bool(re.match(r"^(unit|module|chapter)\s*[-:]?\s*(\d+|[ivx]+)", line.lower()))


def looks_like_subject(line: str) -> bool:
    if len(line) > 60:
        return False
    if looks_like_unit(line):
        return False
    if len(line.split()) > 8:
        return False
    # Subject usually not too short and not bullet-like
    return line[0].isupper() and not re.match(r"^[-•*]", line)


def looks_like_bullet(line: str) -> bool:
    return bool(re.match(r"^[-•*]\s+", line))


def is_valid_topic(line: str) -> bool:
    if len(line) < 2 or len(line) > MAX_TOPIC_LENGTH:
        return False
    return True


def split_topics(text: str) -> List[str]:
    parts = re.split(r",|;", text)
    return [normalize(p) for p in parts if is_valid_topic(normalize(p))]


class ParserState:
    def __init__(self):
        self.current_subject: Optional[Dict] = None
        self.current_unit: Optional[Dict] = None
        self.has_seen_unit = False


def ensure_subject(state: ParserState, syllabus: List[Dict]):
    if not state.current_subject:
        state.current_subject = {"subject": "General", "units": []}
        syllabus.append(state.current_subject)


def ensure_unit(state: ParserState):
    if not state.current_unit:
        state.current_unit = {"unit": "Unit 1", "topics": []}
        state.current_subject["units"].append(state.current_unit)


def parse_syllabus(raw_text: str) -> List[Dict]:
    lines = raw_text.splitlines()
    syllabus: List[Dict] = []
    state = ParserState()

    for raw in lines:
        line = normalize(raw)
        if not line:
            continue

        # ===== SUBJECT =====
        if looks_like_subject(line) and not state.has_seen_unit:
            state.current_subject = {"subject": line, "units": []}
            syllabus.append(state.current_subject)
            state.current_unit = None
            continue

        ensure_subject(state, syllabus)

        # ===== UNIT (with inline topics) =====
        if looks_like_unit(line) and ":" in line:
            unit_part, topic_part = line.split(":", 1)
            unit_name = normalize(unit_part)
            topics = split_topics(topic_part)

            state.current_unit = {"unit": unit_name, "topics": topics}
            state.current_subject["units"].append(state.current_unit)
            state.has_seen_unit = True
            continue

        # ===== UNIT (standalone) =====
        if looks_like_unit(line):
            state.current_unit = {"unit": line, "topics": []}
            state.current_subject["units"].append(state.current_unit)
            state.has_seen_unit = True
            continue

        # ===== TOPICS =====
        ensure_unit(state)

        # Bullet topics
        if looks_like_bullet(line):
            topic = normalize(re.sub(r"^[-•*]\s+", "", line))
            if is_valid_topic(topic):
                state.current_unit["topics"].append(topic)
            continue

        # Comma-separated topics (only split if clearly multiple topics)
        comma_topics = split_topics(line)
        if len(comma_topics) >= 3:
            state.current_unit["topics"].extend(comma_topics)
            continue

        # Plain topic
        if is_valid_topic(line):
            state.current_unit["topics"].append(line)

    return syllabus


def flatten_syllabus(parsed: List[Dict]) -> List[Dict]:
    flat = []
    seen = set()

    for subject in parsed:
        subject_name = subject["subject"]

        for unit in subject["units"]:
            unit_name = unit["unit"]

            for topic in unit["topics"]:
                key = (subject_name.lower(), topic.lower())
                if key in seen:
                    continue

                seen.add(key)
                flat.append({
                    "subject": subject_name,
                    "unit": unit_name,
                    "name": topic,
                    "difficulty": 3,
                    "importance": 3,
                })

    return flat

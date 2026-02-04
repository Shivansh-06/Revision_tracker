# app/syllabus.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.dependencies import get_current_user
from app.schemas import SyllabusParseRequest
from app.syllabus_parser import parse_syllabus, flatten_syllabus

router = APIRouter(prefix="/syllabus", tags=["syllabus"])

@router.post("/parse")
async def parse_syllabus_preview(
    payload: SyllabusParseRequest,
    user=Depends(get_current_user),
):
    parsed = parse_syllabus(payload.text)
    flat_topics = flatten_syllabus(parsed)

    return {
        "count": len(flat_topics),
        "topics": flat_topics
    }





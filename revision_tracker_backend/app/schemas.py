# app/schemas.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import UUID
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class TopicCreate(BaseModel):
    subject: str
    unit: Optional[str] = None
    name: str
    difficulty: int = Field(ge=1, le=5)
    importance: int = Field(ge=1, le=5)

class TopicRead(BaseModel):
    id: UUID
    subject: str
    unit: Optional[str] = None
    name: str
    difficulty: int
    importance: int
    created_at: datetime
    last_revised: Optional[datetime] = None

    class Config:
        from_attributes = True

class RevisionCreate(BaseModel):
    topic_id: UUID
    confidence: int = Field(ge=1, le=5)

class SyllabusParseRequest(BaseModel):
    text: str

class TopicBulkCreate(BaseModel):
    subject: str
    unit: Optional[str] = None
    name: str
    difficulty: int = 3
    importance: int = 3
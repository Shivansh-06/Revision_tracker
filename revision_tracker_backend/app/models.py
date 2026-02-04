# app/models.py
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    priority_mode = Column(String, nullable=False, default="balanced")  # "balanced", "importance", "difficulty"

class Topic(Base):
    __tablename__ = "topics"
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_user_topic"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    subject = Column(String, nullable=False)
    unit = Column(String, nullable=True)  # Added unit
    name = Column(String, nullable=False)

    difficulty = Column(Integer, nullable=False)   # 1–5
    importance = Column(Integer, nullable=False)   # 1–5

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_revised = Column(DateTime(timezone=True), nullable=True)  # Added last_revised

class Revision(Base):
    __tablename__ = "revisions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic_id = Column(UUID(as_uuid=True), ForeignKey("topics.id"), nullable=False)

    confidence = Column(Integer, nullable=False)  # 1–5
    revised_at = Column(DateTime(timezone=True), server_default=func.now())

    topic = relationship("Topic", backref="revisions")


from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Enum as SAEnum
from enum import Enum as PyEnum
from config.database.session import Base

class BoardType(PyEnum):
    BACKLOG = "BACKLOG"
    SPRINT_TERM = "SPRINT_TERM"
    IN_PROGRESS = "IN_PROGRESS"
    REVIEW = "REVIEW"
    DONE = "DONE"
    ADDITIONAL_WORK = "ADDITIONAL_WORK"
    BLOCK="BLOCK"

class BoardORM(Base):
    __tablename__ = "board"

    id = Column(Integer, primary_key=True, index=True)
    board_type = Column(SAEnum(BoardType, native_enum=True), nullable=False, index=True)
    user_id = Column(String(36), nullable=False)

    title = Column(String(255), nullable=False)
    content = Column(String(2000), nullable=False)
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

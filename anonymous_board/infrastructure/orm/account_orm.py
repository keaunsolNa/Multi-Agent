from uuid import uuid4
from sqlalchemy import Column, Integer, String, DateTime, Enum as SAEnum
from enum import Enum as PyEnum
from datetime import datetime

from config.database.session import Base

class OAuthProvider(PyEnum):
    GOOGLE = "GOOGLE"
    NAVER = "NAVER"
    KAKAO = "KAKAO"

class YN(PyEnum):
    Y = "Y"
    N = "N"

class AccountORM(Base):
    __tablename__ = "account"

    id = Column(String(36), primary_key=True, index=True)
    oauth_type = Column(SAEnum(OAuthProvider, native_enum=True), nullable=False, index=True)

    nickname = Column(String(255), nullable=True)
    name = Column(String(255), nullable=True)
    profile_image = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone_number = Column(String(255), nullable=True)
    active_status = Column(SAEnum(YN, native_enum=True), nullable=True)

    role_id = Column(String(255), nullable=True)    ## TODO 권한 관련 추가 작업 필요

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<AccountORM id={self.id} email={self.email} oauth_type={self.oauth_type} nickname={self.nickname}>"
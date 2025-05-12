from sqlalchemy import Column, String, Boolean, DateTime
from .base import BaseModel
from datetime import datetime

class User(BaseModel):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    last_login = Column(DateTime, default=None)
    session_token = Column(String, nullable=True, index=True) 
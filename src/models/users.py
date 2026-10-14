from pydantic import BaseModel, ConfigDict, EmailStr
from sqlalchemy import Column, Integer, String
from src.utils.db import base


class User(base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)


class UserCreate(BaseModel):
    """Model for creating a user - includes sensitive password"""
    name: str
    email: EmailStr
    password: str  # Sensitive - will NOT be returned


class UserResponse(BaseModel):
    """Model for API response - password is excluded"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    # password is NOT included! 🔐


class UserUpdate(BaseModel):
    """Model for updating a user"""
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None

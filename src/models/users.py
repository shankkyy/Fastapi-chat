from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    """Model for creating a user - includes sensitive password"""
    name: str
    email: EmailStr
    password: str  # Sensitive - will NOT be returned


class UserResponse(BaseModel):
    """Model for API response - password is excluded"""
    id: int
    name: str
    email: str
    # password is NOT included! 🔐


class UserUpdate(BaseModel):
    """Model for updating a user"""
    name: str = None
    email: EmailStr = None
    password: str = None

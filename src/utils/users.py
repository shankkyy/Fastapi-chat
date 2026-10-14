from sqlalchemy.orm import Session
from src.models.users import User


def find_user_by_id(db: Session, user_id: int):
    """Find user by ID"""
    return db.get(User, user_id)


def find_user_by_email(db: Session, email: str):
    """Find user by email"""
    return db.query(User).filter(User.email == email).first()

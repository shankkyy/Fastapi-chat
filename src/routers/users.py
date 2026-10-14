from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from src.models.users import User, UserCreate, UserResponse, UserUpdate
from src.utils.db import get_db
from src.utils.users import find_user_by_id, find_user_by_email

router = APIRouter()


@router.post("/users/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.

    - Accepts password in request (UserCreate model)
    - Returns response WITHOUT password (UserResponse model)
    - Stores password in the database but never exposes it
    """
    if find_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(name=user.name, email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/users/", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db)):
    """
    List all users.

    - Returns all users WITHOUT passwords
    - response_model ensures passwords are never included
    """
    return db.query(User).all()


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a specific user by ID.

    - Finds user from the database
    - Returns without password
    """
    user = find_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """
    Update a user by ID.

    - Can update name, email, password
    - Returns updated user WITHOUT password
    """
    user = find_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    updates = user_update.model_dump(exclude_unset=True)
    if "email" in updates:
        existing = find_user_by_email(db, updates["email"])
        if existing and existing.id != user.id:
            raise HTTPException(status_code=400, detail="Email already registered")

    for field, value in updates.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


@router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user by ID.
    """
    user = find_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return None


# ============= DEBUG ENDPOINT (Remove in production) =============

@router.get("/debug/all-users-with-passwords")
def debug_view_all_users(db: Session = Depends(get_db)):
    """
    DEBUG ONLY - Shows all users WITH passwords.
    This endpoint demonstrates that passwords ARE stored,
    but NEVER exposed through normal API responses.

    IMPORTANT: Remove this endpoint in production!
    """
    users = db.query(User).all()
    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "password": user.password,
        }
        for user in users
    ]

from fastapi import APIRouter, HTTPException
from typing import List
from src.models.users import UserCreate, UserResponse, UserUpdate
from src.storage import users_db
from src.utils.users import get_next_id, find_user_by_id, find_user_by_email

router = APIRouter()


@router.post("/users/", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate):
    """
    Create a new user.
    
    - Accepts password in request (UserCreate model)
    - Returns response WITHOUT password (UserResponse model)
    - Stores password in memory but never exposes it
    """
    
    # Check if user already exists
    if find_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user object with ID
    new_user = {
        "id": get_next_id(),
        "name": user.name,
        "email": user.email,
        "password": user.password  # Stored but NOT returned
    }
    
    # Store in memory
    users_db.append(new_user)
    
    # Return only non-sensitive fields (FastAPI handles this with response_model)
    return new_user


@router.get("/users/", response_model=List[UserResponse])
async def list_users():
    """
    List all users.
    
    - Returns all users WITHOUT passwords
    - response_model ensures passwords are never included
    """
    # Even though users_db contains passwords,
    # FastAPI strips them out before sending response
    return users_db


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """
    Get a specific user by ID.
    
    - Finds user from local storage
    - Returns without password
    """
    user = find_user_by_id(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: UserUpdate):
    """
    Update a user by ID.
    
    - Can update name, email, password
    - Returns updated user WITHOUT password
    """
    user = find_user_by_id(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update only provided fields
    if user_update.name:
        user["name"] = user_update.name
    if user_update.email:
        user["email"] = user_update.email
    if user_update.password:
        user["password"] = user_update.password
    
    return user


@router.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int):
    """
    Delete a user by ID.
    """
    user = find_user_by_id(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    users_db.remove(user)
    return None


# ============= DEBUG ENDPOINT (Remove in production) =============

@router.get("/debug/all-users-with-passwords")
async def debug_view_all_users():
    """
    DEBUG ONLY - Shows all users WITH passwords.
    This endpoint demonstrates that passwords ARE stored,
    but NEVER exposed through normal API responses.
    
    IMPORTANT: Remove this endpoint in production!
    """
    return users_db


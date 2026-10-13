import src.storage as storage


def get_next_id():
    """Generate next user ID"""
    current_id = storage.next_user_id
    storage.next_user_id += 1
    return current_id


def find_user_by_id(user_id: int):
    """Find user by ID"""
    for user in storage.users_db:
        if user["id"] == user_id:
            return user
    return None


def find_user_by_email(email: str):
    """Find user by email"""
    for user in storage.users_db:
        if user["email"] == email:
            return user
    return None

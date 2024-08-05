from core.user_management import fastapi_users
from models.user import User
from fastapi import Depends, HTTPException, status

current_active_user = fastapi_users.current_user(active=True)


def get_current_active_user(user: User = Depends(fastapi_users.current_user(active=True))) -> User:
    """Get current active user with role user"""
    if user.role!= "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to access this resource")
    return user

def get_current_active_admin(user: User = Depends(fastapi_users.current_user(active=True))) -> User:
    """Get current active user with role admin"""
    if user.role!= "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to access this resource")
    return user

__all__ = [
    "current_active_user",
    "get_current_active_user",
    "get_current_active_admin",
]

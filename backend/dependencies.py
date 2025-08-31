from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, database
from .auth import get_current_user  # assuming you already have auth system

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def admin_only(current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user

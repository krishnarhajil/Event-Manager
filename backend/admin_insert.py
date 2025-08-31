# backend/admin_insert.py
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models import User
from passlib.context import CryptContext
from backend.auth import get_password_hash

def create_admin():
    db: Session = SessionLocal()
    try:
        # hash the password same way as registration endpoint
        hashed_password = get_password_hash("admin123")  # 🔑 choose your password
        admin_user = User(
            name="Admin User",
            email="admin@example.com",
            hashed_password=hashed_password,
            role="admin"
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        print(f"✅ Admin user created: {admin_user.email}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()

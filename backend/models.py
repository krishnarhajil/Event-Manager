from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from .database import Base
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable = False)
    date = Column(String, nullable = False)
    location = Column(String, nullable = False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    attendances = relationship("Attendance", back_populates="event", cascade = "all,delete")

class User(Base):
    __tablename__ = "users"   
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False) 
    role = Column(String, default="user", nullable = False)

    attendances = relationship("Attendance", back_populates="user")



class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key = True, index = True)
    #attendee_name = Column(String, nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    check_in_time = Column(DateTime, default = datetime.utcnow)
    
    event = relationship("Event", back_populates = "attendances")
    user = relationship("User", back_populates="attendances")

    __table_args__ = (UniqueConstraint("event_id", "user_id", name = "unique_attendance"),)
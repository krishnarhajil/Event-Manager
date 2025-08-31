from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from .. import models, database
from ..auth import get_current_user
from ..database import get_db
from ..dependencies import admin_only
from ..utils.attendance_qr import generate_attendance_qr

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.get("/scan/{event_id}", response_class=HTMLResponse)
def mark_attendance(
    event_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if event exists
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        return "<h3 style='color:red'>❌ Event not found</h3>"

    # Check for duplicate attendance
    existing = db.query(models.Attendance).filter(
        models.Attendance.event_id == event_id,
        models.Attendance.user_id == current_user.id
    ).first()

    if existing:
        return f"<h3>✅ {current_user.username} already marked for {event.name}</h3>"

    # Create new attendance entry
    attendance = models.Attendance(event_id=event_id, user_id=current_user.id)
    db.add(attendance)
    db.commit()
    db.refresh(attendance)

    return f"<h3>✅ {current_user.username} marked now for {event.name}</h3>"


@router.get("/{event_id}")
def get_attendance(
    event_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        return {"status": "error", "message": "Event not found"}

    attendance_list = db.query(models.Attendance).filter(
        models.Attendance.event_id == event_id
    ).all()

    attendees = []
    for a in attendance_list:
        attendees.append({
            "user_id": a.user.id,
            "name": a.user.username,
            "check_in_time": a.check_in_time,
        })

    return {
        "status": "ok",
        "event": event.name,
        "attendees": attendees
    }


@router.post("/generate_qr/{event_id}")
def generate_attendance_qr_endpoint(
    event_id: int,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(admin_only)
):
    # check if event exists
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    qr_path = generate_attendance_qr(event.id)
    return {
        "event_id": event.id,
        "attendance_qr_path": qr_path
    }

@router.get("/my_attendance")
def get_my_attendance(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Fetch all attendance records for the current user
    records = db.query(models.Attendance).filter(
        models.Attendance.user_id == current_user.id
    ).all()

    if not records:
        return {
            "status": "ok",
            "message": "No attendance records found",
            "attendances": []
        }

    history = []
    for record in records:
        history.append({
            "event_id": record.event.id,
            "event_name": record.event.name,
            "check_in_time": record.check_in_time,
        })

    return {
        "status": "ok",
        "user": current_user.username,
        "attendances": history
    }

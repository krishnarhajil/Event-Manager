from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database, schemas
from ..dependencies import admin_only
from ..auth import get_current_user

router = APIRouter(tags=["Events"])


@router.post("/", response_model=schemas.Event)
def create_event(
    event: schemas.EventCreate,
    db: Session = Depends(database.get_db),
    current_admin: models.User = Depends(admin_only)
):
    new_event = models.Event(**event.dict())
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event


@router.get("/", response_model=list[schemas.Event])
def list_events(db: Session = Depends(database.get_db)):
    return db.query(models.Event).all()


@router.get("/{event_id}", response_model=schemas.Event)
def get_event(event_id: int, db: Session = Depends(database.get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.put("/{event_id}", response_model=schemas.Event)
def update_event(
    event_id: int,
    updated: schemas.EventCreate,
    db: Session = Depends(database.get_db),
    current_admin: models.User = Depends(admin_only)
):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    for key, value in updated.dict().items():
        setattr(event, key, value)

    db.commit()
    db.refresh(event)
    return event


@router.delete("/{event_id}")
def delete_event(
    event_id: int,
    db: Session = Depends(database.get_db),
    current_admin: models.User = Depends(admin_only)
):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    db.delete(event)
    db.commit()
    return {"status": "success", "message": "Event deleted"}

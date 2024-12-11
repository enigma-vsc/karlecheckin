from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..model import models
from .. import schemas
from ..database import get_db
from sqlalchemy import select

router = APIRouter(prefix="/customer", tags=["customer"])

@router.get("/rooms", response_model=list[schemas.RoomResponse])
async def get_available_rooms(db: Session = Depends(get_db)):
    rooms = db.query(models.Room).filter(models.Room.availability == True).all()
    return rooms


@router.post("/available-rooms")
def get_available_rooms(request: schemas.RoomAvailabilityRequest, db: Session = Depends(get_db)):
    subquery = select(models.Booking.room_id).filter(
        models.Booking.check_in < request.check_out,
        models.Booking.check_out >= request.check_in
    ).subquery()



    available_rooms = db.query(models.Room).filter(
        ~models.Room.id.in_(subquery)
    ).all()

    return available_rooms


@router.post("/users", response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/bookings", response_model=schemas.BookingResponse)
async def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    db_booking = models.Booking(**booking.dict())
    
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking



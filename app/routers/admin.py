from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..model import models
import app.schemas as schemas
from ..database import get_db

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/rooms/{room_id}", response_model=schemas.RoomResponse)
async def get_booking(room_id: int, db: Session = Depends(get_db)):
    db_booking = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_booking

@router.get("/rooms", response_model=list[schemas.RoomResponse])
async def get_all_rooms(db: Session = Depends(get_db)):
    rooms = db.query(models.Room).all()
    return rooms


@router.post("/rooms", response_model=schemas.RoomResponse)
async def add_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    db_room = models.Room(**room.dict())
    # if isinstance(db_room["features"], str):  # Check if it's still a string
    #     db_room["features"] = db_room["features"].split(", ")
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

@router.put("/rooms/{room_id}", response_model=schemas.RoomResponse)
async def update_room(room_id: int, room: schemas.RoomUpdate, db: Session = Depends(get_db)):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")
    for key, value in room.dict(exclude_unset=True).items():
        setattr(db_room, key, value)
    db.commit()
    db.refresh(db_room)
    return db_room

@router.delete("/rooms/{room_id}")
async def delete_room(room_id: int, db: Session = Depends(get_db)):
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")
    db.delete(db_room)
    db.commit()
    return {"message": "Room deleted successfully"}


@router.get("/bookings/{booking_id}", response_model=schemas.BookingResponse)
async def get_booking(booking_id: int, db: Session = Depends(get_db)):
    db_booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking

@router.get("/bookings", response_model=list[schemas.BookingResponse])
async def get_all_bookings(db: Session = Depends(get_db)):
    bookings = db.query(models.Booking).all()
    return bookings

@router.delete("/bookings/{booking_id}")
async def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    db_booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    db_booking.status = "Cancelled"
    db.commit()
    return {"message": "Booking cancelled successfully"}


@router.get("/users/{user_id}", response_model=schemas.UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_user


@router.post("/rooms", response_model=schemas.RoomResponse)
async def add_room(room: schemas.RoomCreate, db: Session = Depends(get_db)):
    db_room = models.Room(**room.dict())
    # if isinstance(db_room["features"], str):  # Check if it's still a string
    #     db_room["features"] = db_room["features"].split(", ")
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


@router.get("/users", response_model=list[schemas.UserResponse])
async def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.put("/users/{user_id}", response_model=schemas.UserResponse)
async def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

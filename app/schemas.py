from typing import Optional, List
from pydantic import BaseModel, Field, validator
from datetime import date

class RoomBase(BaseModel):
    type: str
    price: float
    description: Optional[str] = None
    features: Optional[str] = Field(None)  # Updated to List[str]
    availability: Optional[bool] = True

class RoomCreate(RoomBase):
    pass

class RoomUpdate(RoomBase):
    pass

class RoomResponse(RoomBase):
    id: int

    class Config:
        from_attributes = True

class RoomAvailabilityRequest(BaseModel):
    check_in: str
    check_out: str

class UserBase(BaseModel):
    email: str
    password_hash: str
    role: Optional[str] = Field("customer")

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True



class BookingBase(BaseModel):
    user_id: int
    room_id: int
    check_in: str
    check_out: str

class BookingCreate(BookingBase):
    pass

class BookingResponse(BookingBase):
    id: int
    status: str

    class Config:
        from_attributes = True

        # Validator to convert datetime.date to string
    @validator("check_in", "check_out", pre=True)
    def convert_date_to_string(cls, value):
        if isinstance(value, date):
            return value.isoformat()  # Converts to 'YYYY-MM-DD'
        return value

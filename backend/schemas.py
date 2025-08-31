from pydantic import BaseModel, EmailStr
from datetime import datetime

class EventBase(BaseModel):
    name : str
    description : str | None = None

class Event(EventBase):
    id: int

    class Config:
        from_attributes = True


class EventCreate(EventBase):

    location : str
    date : datetime

class EventOut(EventBase):
    id : int
    name : str
    location : str
    date : datetime

    class Config:
        from_attributes = True

class EventWithQR(BaseModel):
    event: EventOut
    qr_code_path : str


class UserBase(BaseModel):
    name: str
    email: EmailStr  

class UserCreate(UserBase):
    username: str
    email: str
    password: str 

class UserLogin(BaseModel):
    email: str
    password: str
    
class UserOut(UserBase):
    id: int
    name: str
    email: str
    role: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from .enums import Gender


class UserBase(BaseModel):
    email: str
    username: str

    dob: Optional[date] = None
    gender: Optional[Gender] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    profile_pic: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: str
    dob: Optional[date] = None
    gender: Optional[Gender] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    profile_pic: Optional[str] = None


class User(UserBase):
    id: int
    created_date: datetime

    class Config:
        orm_mode = True

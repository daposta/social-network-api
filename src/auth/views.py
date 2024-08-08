from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime
from .schemas import UserCreate, UserUpdate, User as UserSchema
from ..database import get_db
from .service import existing_user, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])
# apis
# sign up
@router.post("signup", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db))
    #check for existing user
    db_user = await existing_user(db, user.username, user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Username already in use")
     

# login to generate token
# get user
# update user
# reset password

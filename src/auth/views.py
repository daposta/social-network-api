from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime
from .schemas import UserCreate, UserUpdate, User as UserSchema
from ..database import get_db
from .service import existing_user, create_access_token, get_current_user,create_user as create_use_svc, authenticate


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
    db_user = create_use_svc(db, user)
    access_token = create_access_token(user.username, db_user.id)
    return  {
        "access_token": access_token,
        "token_type": "bearer",
        "username" : user.name
    }

# login to generate token
@router.post('/token', status_code=status.HTTP_200_OK)
async def login(formData: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = await authenticate(db, formData.username, formData.password)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Incorrect username  or password")
    
    access_token = await create_access_token(db_user.username, db_user.id )
    return {"access_token": access_token, "token_type": "bearer",}

# get user
# update user
# reset password

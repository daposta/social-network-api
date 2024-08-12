from fastapi import Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
from .schemas import UserCreate, UserUpdate

from .models import User

# used for hashing password
bcrypt_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)  # used for hashing password
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/v1/auth/token")
SECRET_KEY = "secretkey"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINS = 60 * 24 * 1  # 1day


# check for existing user
async def existing_user(db: Session, username: str, email: str):
    db_user = db.query(User).filter(User.email == email).first()
    db_user = db.query(User).filter(User.username == username).first()
    return db_user


# create access token
async def create_access_token(username: str, id: int):
    encode = {"sub": username, "id": id}
    expires = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINS)
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


# get current user from token
async def get_current_user(db: Session, token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        id: str = payload.get("id")
        expires: datetime = payload.get("exp")

        if datetime.fromtimestamp(expires) < datetime.now():
            return None

        if username is None or id is None:
            return None

        return db.query(User).filter(User.id == id).first()
    except JWTError:
        return None


# get user from user id
async def get_user_from_user_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


# def create user
async def create_user(db: Session, user: UserCreate):
    db_user = User(
        email=user.email.lower().strip(),
        username=user.username.lower().strip() or user.username,
        hashed_password=bcrypt_context.hash(user.password),
        dob=user.dob or None,
        gender=user.gender or None,
        bio=user.bio or None,
        location=user.location or None,
        profile_pic=user.profile_pic or None,
        name=user.name or None,
    )
    db.add(db_user)
    db.commit()
    return db_user


# authenticate
async def authenticate(db: Session, username: str, password: str):
    db_user = await existing_user(db, username, "")
    if not db_user:
        return None
    if not bcrypt_context.verify(password, db_user.hashed_password):
        return None
    return db_user


# update user
async def update_user(db: Session, db_user: User, user_update: UserUpdate):
    db_user.bio = user_update.bio or db_user.bio
    db_user.name = user_update.name or db_user.name
    db_user.gender = user_update.gender or db_user.gender
    db_user.dob = user_update.dob or db_user.dob
    db_user.location = user_update.location or db_user.location
    db_user.profile_pic = user_update.profile_pic or db_user.profile_pic
    db.commit()

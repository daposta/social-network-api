from fastapi import Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
from .schemas import UserCreate

from .models import User

# used for hashing password
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="author")
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
        payload = jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])
        username: str = payload.get("sub")
        id: str = payload.get("id")
        expires: datetime = payload.get("exp")

        if datetime(expires) < datetime.now():
            return None

        if username is None or id is None:
            return None

        return db.query(User).filter(User.id=id).first()
    except JWTError:
        return None


# get user from user id
async def get_user_from_user_id(db: Session, user_id: int):
    return db.query(User).filter(User.id=user_id).first()


# def create user
async def create_user(db: Session, user: UserCreate):
    db_user = User(email=user.email.lower().strip(), username=user.username.lower().strip(), hashed_password=bcrypt_context.hash(
        user.password), db=user.db or None, gender=user.gender or None, 
        bio = user.bio or None, profile_pic=user.profile_pic or None, name = user.name or None)
    db.add(db_user)
    db.commit()
    return db_user


# authenticate
async def authenticate(db:Session, username:str, password: str):
    db_user = await existing_user(db, username, "")
    if not db_user:
        return None
    if not bcrypt_context.verify(password, db_user.password):
        return None
    return db_user
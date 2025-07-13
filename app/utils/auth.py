from fastapi import Depends, HTTPException, status, Request
from app.database.database import get_db
from app.models.user import User
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from dotenv import load_dotenv
import bcrypt
import os

# Loading Sensitive Variables from .env file
load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") 
HASH_ALGORITHM = os.getenv("HASH_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Function to Hash Passwords
def hash_password(password: str):
    salt = bcrypt.gensalt(10)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

# Function to verify a plain password against a hashed password stored in DB
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Function to create a JWT Token
def create_access_token(data: dict, expired_delta: timedelta = None):
    token_data = data.copy()
    if expired_delta is not None:
        expire = datetime.now(timezone.utc) + expired_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data.update({"exp": expire})
    encoded_jwt = jwt.encode(token_data, JWT_SECRET_KEY, algorithm=HASH_ALGORITHM)
    return encoded_jwt

# Function to verify a JWT token, i.e check it from a valid user and return the user data
def get_current_user(request: Request, db: Session = Depends(get_db)):
    token_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Couldn't verify access token.",
    )

    access_token = request.cookies.get("access_token")
    if not access_token:
        raise token_error

    try:
        payload = jwt.decode(access_token, JWT_SECRET_KEY, algorithms=[HASH_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise token_error
    except JWTError:
        raise token_error
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise token_error
    
    return user


#
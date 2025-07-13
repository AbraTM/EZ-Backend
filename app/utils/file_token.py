from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from jose import jwt, JWTError
import os

load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
HASH_ALGORITHM = os.getenv("HASH_ALGORITHM")
DOWNLOAD_TOKEN_EXPIRE_MINUTES = int(os.getenv("DOWNLOAD_TOKEN_EXPIRE_MINUTES"))

def generate_download_token(file_id: str, expire_minutes: int = None):
    token_data = {"file_id" : file_id}
    if expire_minutes is not None:
        expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=DOWNLOAD_TOKEN_EXPIRE_MINUTES)
    token_data.update({"exp": expire})
    encoded_jwt = jwt.encode(token_data, JWT_SECRET_KEY, algorithm=HASH_ALGORITHM)
    return encoded_jwt

def verify_download_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[HASH_ALGORITHM])
        file_id: str = payload.get("file_id")
        if file_id is None:
            return None
        return file_id
    except JWTError:
        return None
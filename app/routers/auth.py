from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin
from app.models.user import User
from app.database.database import get_db
from app.utils import auth

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
def signup(user_data: UserCreate, db: Session = Depends(get_db)):

    # Firstly, check if a user with the email provided already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered.")
    
    # Hash Password (So, we don't save the actual user password int the db, but an encrypted one)
    hashed_pw = auth.hash_password(user_data.password)

    # Create new user object
    new_user = User(
        name = user_data.name,
        email = user_data.email,
        password = hashed_pw,
        user_type = user_data.user_type.value,
        is_verified = False
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Creating a JWT Token and setting that token as an httpOnly cookie to allow further access
    token_data = {"sub": str(new_user.id), "user_type": new_user.user_type.value}
    access_token = auth.create_access_token(token_data)
    response = Response(content='{"message": "Signup successful"}', media_type="application/json")
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite='lax',
        max_age=60*60, # 1hr
    )
    return response

@router.post("/login")
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    
    # Checking if a user exists
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="User doesn't exists.")
    
    if not auth.verify_password(login_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect password.")
    
    # Creating a JWT token
    token_data = {"sub": str(user.id), "user_type": user.user_type.value}
    access_token = auth.create_access_token(token_data)
    response = Response(content='{"message": "Login successful"}', media_type="application/json")
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60*60, # 1hr
    )
    return response
    

@router.post("/logout")
def logout(response: Response):
    response = Response(content='{"message": "Logged out successfully."}', media_type="application/json")
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return response
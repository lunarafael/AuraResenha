from sqlalchemy.orm import Session
from fastapi import HTTPException, status
# from app import models, schemas
from app.models import user
from app.schemas import user as user_schemas
from app.core.security import get_password_hash, verify_password, create_access_token

def register_user(db: Session, user_in: user_schemas.UserCreate):
    existing_user = db.query(user.User).filter(
        (user.User.email == user_in.email) |
        (user.User.username == user_in.username)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered.")

    hashed_pw = get_password_hash(user_in.password)
    db_user = user.User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_pw
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(user.User).filter(user.User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")
    return user

def create_user_token(user: user.User):
    return create_access_token({"sub": str(user.id)})

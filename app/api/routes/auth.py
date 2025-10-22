from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db.session import get_db
from app import schemas
from app.services import auth as auth_service
from app.core.security import decode_access_token
from app.models.user import User

router = APIRouter()

@router.post("/register", response_model=schemas.user.UserOut)
def register(user_in: schemas.user.UserCreate, db: Session = Depends(get_db)):
    print(type(user_in.password), user_in.password)
    return auth_service.register_user(db, user_in)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    token = auth_service.create_user_token(user)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.user.UserOut)
def read_users_me(token: str, db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = int(payload.get("sub"))
    user = db.query(User).get(user_id)
    return user

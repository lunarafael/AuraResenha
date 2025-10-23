from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db.session import get_db
from app import schemas
from app.services import auth as auth_service
from app.core.security import decode_access_token
from app.models.user import User

router = APIRouter()

@router.post("/register", 
             response_model=schemas.user.UserOut,
             summary="Register a new user",
             description="Create a new user account by providing a username, email, and password.",
             response_description="The created user's public information."
)
def register(user_in: schemas.user.UserCreate, db: Session = Depends(get_db)):
    """Register a new user.

    This endpoint creates a new user in the database.
    It returns the user's public data (excluding password).
    """
    print(type(user_in.password), user_in.password)
    return auth_service.register_user(db, user_in)

@router.post("/login",
             summary="Login and get access token",
             description="Authenticate a user using username and password. Returns a JWT access token.",
             response_description="Access token for authenticated requests."
)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticate an existing user.

    Returns a Bearer token that must be used in future requests to access protected routes.
    """
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    token = auth_service.create_user_token(user)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me",
            response_model=schemas.user.UserOut,
            summary="Get current authenticated user",
            description="Return the currently authenticated user's information using their token.",
            response_description="The authenticated user's public information."
)
def read_current_user(token: str, db: Session = Depends(get_db)):
    """Get the current user based on a valid JWT token."""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = int(payload.get("sub"))
    user = db.query(User).get(user_id)
    return user

from fastapi import APIRouter, Depends, HTTPException, status, Query, Header
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import decode_access_token
from app import schemas
from app.models.user import User
from app.services import post as post_service

router = APIRouter()

def get_current_user(authorization: str = Header(...), db: Session = Depends(get_db)):
    """
    Get current user from Bearer token in Authorization header
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization.replace("Bearer ", "")
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = int(payload.get("sub"))
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=schemas.post.PostOut)
def create_post(post_in: schemas.post.PostCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return post_service.create_post(db, current_user.id, post_in)

@router.get("/", response_model=list[schemas.post.PostOut])
def get_posts(skip: int = Query(0, ge=0), limit: int = Query(20, le=100), db: Session = Depends(get_db)):
    return post_service.get_all_posts(db, skip, limit)

@router.get("/{post_id}", response_model=schemas.post.PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = post_service.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{post_id}", response_model=schemas.post.PostOut)
def update_post(post_id: int, post_in: schemas.post.PostUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    post = post_service.update_post(db, post_id, post_in, current_user.id)
    if not post:
        raise HTTPException(status_code=403, detail="Not authorized or post not found")
    return post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    deleted = post_service.delete_post(db, post_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=403, detail="Not authorized or post not found")
    return
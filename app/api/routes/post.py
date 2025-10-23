from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import decode_access_token
from app import schemas
from app.models.user import User
from app.services import post as post_service

router = APIRouter()

def get_current_user(token: str, db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = int(payload.get("sub"))
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/",
            response_model=schemas.post.PostOut,
            summary="Create a new post",
            description="Create a new post linked to the authenticated user."
)
def create_post(post_in: schemas.post.PostCreate, token: str,db: Session = Depends(get_db)):
    """Create a new post."""
    current_user = get_current_user(token, db)
    return post_service.create_post(db, current_user.id, post_in)

@router.get("/",
            response_model=list[schemas.post.PostOut],
            summary="Get all posts",
            description="Retrieve all posts with optional pagination (skip, limit)."
)
def get_posts(skip: int = Query(0, ge=0), limit: int = Query(20, le=100), db: Session = Depends(get_db)):
    """List all posts."""
    return post_service.get_all_posts(db, skip, limit)

@router.get("/{post_id}",
            response_model=schemas.post.PostOut,
            summary="Get a post by ID"
)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Retrieve a single post by its ID."""
    post = post_service.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{post_id}",
            response_model=schemas.post.PostOut,
            summary="Update a post"
)
def update_post(post_id: int, post_in: schemas.post.PostUpdate, token: str, db: Session = Depends(get_db)):
    """Update a post (only the author can edit)."""
    current_user = get_current_user(token, db)
    post = post_service.update_post(db, post_id, post_in, current_user.id)
    if not post:
        raise HTTPException(status_code=403, detail="Not authorized or post not found")
    return post

@router.delete("/{post_id}",
            status_code=status.HTTP_204_NO_CONTENT,
            summary="Delete a post"
)
def delete_post(post_id: int, token: str, db: Session = Depends(get_db)):
    """Delete a post (only the author can delete)."""
    current_user = get_current_user(token, db)
    deleted = post_service.delete_post(db, post_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=403, detail="Not authorized or post not found")
    return
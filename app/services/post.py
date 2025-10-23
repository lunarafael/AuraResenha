from sqlalchemy.orm import Session
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate

def create_post(db: Session, author_id: int, post_in: PostCreate):
    post = Post(**post_in.dict(), author_id=author_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

def get_all_posts(db: Session, skip: int = 0, limit: int = 20):
    return db.query(Post).offset(skip).limit(limit).all()

def update_post(db: Session, post_id: int, post_in: PostUpdate, author_id: int):
    post = get_post(db, post_id)
    if not post or post.author_id != author_id:
        return None
    for field, value in post_in.dict().items():
        setattr(post, field, value)
    db.commit()
    db.refresh(post)
    return post

def delete_post(db: Session, post_id: int, author_id: int):
    post = get_post(db, post_id)
    if not post or post.author_id != author_id:
        return None
    db.delete(post)
    db.commit()
    return True

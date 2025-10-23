from fastapi import FastAPI
from app.api.router import api_router
from app.api.routes import auth, post
from app.models.base_class import Base
from app.db.session import engine
from app.db import base

app = FastAPI(title="AuraResenha API")

Base.metadata.create_all(bind=engine)

app.include_router(api_router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(post.router, prefix="/api/v1/posts", tags=["posts"])


@app.get("/")
def root():
    return {"message": "AuraResenha"}
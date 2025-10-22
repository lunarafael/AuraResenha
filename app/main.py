from fastapi import FastAPI
from app.api.router import api_router
from app.models.base_class import Base
from app.db.session import engine
from app.db import base

app = FastAPI(title="AuraResenha API")

Base.metadata.create_all(bind=engine)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "AuraResenha"}
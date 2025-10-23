from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.models.base_class import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    aura_score = Column(Integer, default=0)
    resenha_score = Column(Integer, default=0)

    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comments", back_populates="user", cascade="all, delete-orphan")
    votes = relationship("Vote", back_populates="user", cascade="all, delete-orphan")
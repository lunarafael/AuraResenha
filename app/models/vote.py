from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.base_class import Base

class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))

    aura = Column(Boolean, default=False)
    resenha = Column(Boolean, default=False)

    user = relationship("User", back_populates="votes")
    post = relationship("Post", back_populates="votes")

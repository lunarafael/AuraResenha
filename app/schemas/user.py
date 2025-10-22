from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    is_admin: bool
    aura_score: int
    resenha_score: int

    class Config:
        from_attributes = True

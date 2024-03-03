
from pydantic import BaseModel, EmailStr
from datetime import datetime

# request model
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserCreate(BaseModel):
    email: EmailStr
    password: str

# response model
class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode: True

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode: True

from pydantic import BaseModel

class UserCreate(BaseModel):
    user_id: int
    username: str

class UserUpdate(BaseModel):
    username: str

class User(BaseModel):
    user_id: int
    username: str
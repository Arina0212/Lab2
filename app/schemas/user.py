from pydantic import BaseModel, ConfigDict, EmailStr
from typing import List

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    name: str | None = None

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class UserListResponse(BaseModel):
    users: List[UserResponse]
    total_count: int
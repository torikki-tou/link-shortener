from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    is_superuser: bool = False


class UserCreate(UserBase):
    name: str
    email: str
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: str
    name: str
    email: str


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str

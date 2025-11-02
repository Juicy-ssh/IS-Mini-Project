# schemas.py
from pydantic import BaseModel, EmailStr

# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

# --- User Schemas ---
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(BaseModel):
    email: EmailStr

class UserRegisterResponse(BaseModel):
    username: str
    email: EmailStr
    key: str

class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True

# --- File Schemas ---
class FileInfo(BaseModel):
    id: int
    filename: str
    owner_id: int

    class Config:
        from_attributes = True

class FileUpload(BaseModel):
    recipient_username: str | None = None

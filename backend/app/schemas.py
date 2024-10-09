from pydantic import BaseModel, EmailStr, constr, field_validator, HttpUrl
from typing import Optional
from datetime import datetime
import re

# User schemas
class UserCreate(BaseModel):
    email: EmailStr
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=8)

    @field_validator('password')
    @classmethod
    def password_strength(cls, v):
        """
        Validate password strength:
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        - At least one special character
        """
        if (re.search(r'[A-Z]', v) and
            re.search(r'[a-z]', v) and
            re.search(r'\d', v) and
            re.search(r'[!@#$%^&*(),.?":{}|<>]', v)):
            return v
        raise ValueError('Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character.')

class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    created_at: datetime

    class Config:
        from_attributes = True 

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None

class LogCreate(BaseModel):
    timestamp: datetime
    event: str
    user: str
    ip: str
    site_url: str
    url: str
    method: str
    user_agent: str
    referrer: str
    query_string: str
    remote_addr: str
    request_time: int
    extra: str

class LogOut(BaseModel):
    id: int
    timestamp: datetime
    event: str
    user: str
    ip: str
    site_url: str
    url: str
    method: str
    user_agent: str
    referrer: str
    query_string: str
    remote_addr: str
    request_time: int
    extra: str

    class Config:
        from_attributes = True 
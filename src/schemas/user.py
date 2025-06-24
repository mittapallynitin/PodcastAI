# Request Response Schema for User endpoints
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr = Field(..., description="The user's email address")
    first_name: str = Field(..., description="The user's first name")
    last_name: str = Field(..., description="The user's last name")


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="The user's password")


class UserUpdate(UserBase):
    phone_number: str | None = Field(None, description="The user's phone number")
    date_of_birth: str | None = Field(None, description="The user's date of birth in YYYY-MM-DD format")


class UserFullResponse(UserBase):
    phone_number: str | None = Field(None, description="The user's phone number")
    date_joined: str = Field(..., description="The date the user joined the platform")
    date_of_birth: str | None = Field(None, description="The user's date of birth in YYYY-MM-DD format")


class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="The user's email address")
    password: str = Field(..., min_length=8, description="The user's password for login")


class Token(BaseModel):
    access_token: str = Field(..., description="The access token for the user")
    token_type: str = Field(..., description="The type of the token, usually 'bearer'")


class TokenPayLoad(BaseModel):
    email: str = Field(..., description="The email of the user associated with the token")
    exp: datetime = Field(..., description="The expiration time of the token in minutes")

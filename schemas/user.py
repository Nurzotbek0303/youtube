from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional
import re


class SchemasUser(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=30,
        pattern="^[a-zA-Z0-9_]+$",
        description="Faqat harflar, raqamlar va _",
    )
    email: EmailStr
    password: str = Field(
        ..., min_length=8, max_length=128, description="Kamida 8 ta belgi"
    )

    @validator("password")
    def validate_password(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Parolda kamida bitta katta harf bo'lishi kerak")
        if not re.search(r"[0-9]", v):
            raise ValueError("Parolda kamida bitta raqam bo'lishi kerak")
        return v


class UserResp(BaseModel):
    id: int
    username: str
    email: str
    create_at: datetime
    user_image: Optional[str] = ""

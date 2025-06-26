from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic_settings import BaseSettings


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    role: Optional[str] = None
    id: Optional[int] = None


class TokenData(BaseModel):
    username: EmailStr


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class Settings(BaseSettings):
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        env_file = ".env"

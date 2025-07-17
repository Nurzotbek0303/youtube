from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SchemasShortsLike(BaseModel):
    video_id: int
    is_like: bool


class ShortsLikeResp(BaseModel):
    id: int
    username: str
    shorts_id: int
    video_url: Optional[str] = ""
    is_like: bool
    created_at: datetime

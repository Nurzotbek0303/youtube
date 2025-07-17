from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SchemasLike(BaseModel):
    video_id: int
    is_like: bool


class LikeResp(BaseModel):
    id: int
    username: str
    video_title: str
    file_path: Optional[str] = ""
    thumbnail_path: Optional[str] = ""
    video_views: int
    is_like: bool
    created_at: datetime

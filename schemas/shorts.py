from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ShortsResp(BaseModel):
    id: int
    video_url: Optional[str] = ""
    thumbnail_path: Optional[str] = ""
    channel_name: str
    profile_image: Optional[str] = ""
    like_amount: int
    views: int
    created_at: datetime

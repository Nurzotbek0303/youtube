from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SchemasHistory(BaseModel):
    video_id: int


class HistoryResp(BaseModel):
    id: int
    channel_name: str
    video_title: str
    thumbnail_path: Optional[str] = ""
    video_description: str
    video_id: int
    views: int
    watched_at: datetime

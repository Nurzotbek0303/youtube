from pydantic import BaseModel, Field
from datetime import datetime


class SchemasShortsComment(BaseModel):
    video_id: int
    comment: str = Field(min_length=3, max_length=1000)


class ShortsCommentResp(BaseModel):
    id: int
    comment: str
    channel_name: str
    shortsComent_id: str
    created_at: datetime

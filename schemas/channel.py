from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class SchemasChannel(BaseModel):
    name: str = Field(..., min_length=3, max_length=150)
    description: str = Field(..., min_length=3, max_length=1000)


class MyChannelResp(BaseModel):
    id: int
    user_id: int
    channel_name: str
    channel_description: str
    profile_image: Optional[str] = ""
    banner_image: Optional[str] = ""
    created_at: datetime
    subscription_amount: int


class ChannelResp(BaseModel):
    id: int
    channel_name: str
    channel_description: str
    profile_image: Optional[str] = ""
    banner_image: Optional[str] = ""
    created_at: datetime
    subscription_amount: int

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SchemasSubscription(BaseModel):
    channel_id: int


class MySubscriptionResp(BaseModel):
    id: int
    username: str
    user_image: Optional[str] = ""
    channel_name: str
    created_at: datetime


class SubscriptionResp(BaseModel):
    id: int
    channel_name: str
    channel_profile_image: Optional[str] = ""
    channel_subscription_amount: int
    username: str
    created_at: datetime

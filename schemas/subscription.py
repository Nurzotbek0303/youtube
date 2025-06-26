from pydantic import BaseModel, field_serializer
from datetime import datetime
import pytz


class SchemasSubscription(BaseModel):
    channel_id: int


class SubscriptionResponse(BaseModel):
    id: int
    name: str
    profile_image: str | None
    subscription_amount: int
    username: str
    created_at: datetime

    @field_serializer("created_at")
    def vaqt_tahrirlash(self, value: datetime, _info):
        tashkent_tz = pytz.timezone("Asia/Tashkent")
        if value.tzinfo is None:
            value = pytz.utc.localize(value)

        tashkent_time = value.astimezone(tashkent_tz)
        return tashkent_time.strftime("%d.%m.%Y %H:%M:%S")

    model_config = {"from_attributes": True}


class SubscriptionUser(BaseModel):
    id: int
    username: str
    image: str | None
    name: str
    created_at: datetime

    @field_serializer("created_at")
    def vaqt_tahrirlash(self, value: datetime, _info):
        tashkent_tz = pytz.timezone("Asia/Tashkent")
        if value.tzinfo is None:
            value = pytz.utc.localize(value)

        tashkent_time = value.astimezone(tashkent_tz)
        return tashkent_time.strftime("%d.%m.%Y %H:%M:%S")

    model_config = {"from_attributes": True}

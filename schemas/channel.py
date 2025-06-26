from pydantic import BaseModel, field_serializer
from datetime import datetime
import pytz


class SchemasChannel(BaseModel):
    name: str
    description: str


class ChannelResponse(BaseModel):
    id: int
    user_id: int
    name: str
    description: str
    profile_image: str | None = None
    banner_image: str | None = None
    created_at: datetime
    subscription_amount: int

    @field_serializer("created_at")
    def vaqt_tahrirlash(self, value: datetime, _info):
        tashkent_tz = pytz.timezone("Asia/Tashkent")
        if value.tzinfo is None:
            value = pytz.utc.localize(value)

        tashkent_time = value.astimezone(tashkent_tz)
        return tashkent_time.strftime("%d.%m.%Y %H:%M:%S")

    model_config = {"from_attributes": True}


class ScemasChannelResponse(BaseModel):
    id: int
    name: str
    description: str
    profile_image: str | None = None
    banner_image: str | None = None
    created_at: datetime
    subscription_amount: int

    @field_serializer("created_at")
    def vaqt_tahrirlash(self, value: datetime, _info):
        tashkent_tz = pytz.timezone("Asia/Tashkent")
        if value.tzinfo is None:
            value = pytz.utc.localize(value)

        tashkent_time = value.astimezone(tashkent_tz)
        return tashkent_time.strftime("%d.%m.%Y %H:%M:%S")

    model_config = {"from_attributes": True}

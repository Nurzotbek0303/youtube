from fastapi import Form
from enum import Enum
from pydantic import BaseModel, field_serializer
from datetime import datetime
import pytz


class Category(str, Enum):
    musiqa = "Musiqa"
    talim = "Ta'lim"
    texnologiya = "Texnologiya"
    oyinlar = "O'yinlar"
    yangiliklar = "Yangiliklar"
    kongilochar = "Ko'ngilochar"
    sport = "Sport"
    ilmfan = "Ilm-fan va Tabiat"
    sayohat = "Sayohat"
    pazandachilik = "Oshxona va Pazandachilik"
    moda = "Moda va Go'zallik"
    biznes = "Biznes"
    motivatsiya = "Motivatsiya"
    film = "Filmlar"
    serial = "Seriallar"
    avtomobillar = "Avtomobillar"
    hayvonlar = "Hayvonlar"
    siyosat = "Siyosat"


class UpdateVideo(BaseModel):
    title: str
    description: str
    category: Category


class SchemasVideo(BaseModel):
    title: str
    description: str
    category: Category

    @classmethod
    def as_form(
        cls,
        title: str = Form(...),
        description: str = Form(...),
        category: Category = Form(...),
    ):
        return cls(
            title=title,
            description=description,
            category=category,
        )


class VidyoResponse(BaseModel):
    id: int
    name: str
    profile_image: str | None
    title: str
    description: str
    file_path: str
    thumbnail_path: str
    category: Category
    views: int
    created_at: datetime
    like_amount: int

    @field_serializer("created_at")
    def vaqt_tahrirlash(self, value: datetime, _info):
        tashkent_tz = pytz.timezone("Asia/Tashkent")
        if value.tzinfo is None:
            value = pytz.utc.localize(value)

        tashkent_time = value.astimezone(tashkent_tz)
        return tashkent_time.strftime("%d.%m.%Y %H:%M:%S")

    model_config = {"from_attributes": True}

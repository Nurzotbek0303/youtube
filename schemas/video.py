from fastapi import Form
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


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
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=1000)
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


class MyVideoResp(BaseModel):
    id: int
    name: str
    profile_image: Optional[str] = ""
    title: str
    description: str
    file_path: Optional[str] = ""
    thumbnail_path: Optional[str] = ""
    category: Category
    views: int
    created_at: datetime
    like_amount: int
    duration_video: float
    dislike_amount: int


class VideoResp(BaseModel):
    id: int
    channel_name: str
    profile_image: Optional[str] = ""
    video_title: str
    video_description: str
    file_path: Optional[str] = ""
    thumbnail_path: Optional[str] = ""
    category: Category
    video_views: int
    created_at: datetime
    like_amount: int
    duration_video: float


class CommentResp(BaseModel):
    id: int
    comment: str
    channel_name: str
    comment_id: int
    created_at: datetime

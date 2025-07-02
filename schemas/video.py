from fastapi import Form
from enum import Enum
from pydantic import BaseModel


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

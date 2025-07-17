from fastapi import APIRouter, Depends, UploadFile, HTTPException, Response
from sqlalchemy import delete
from typing import Optional, List

from sqlalchemy.future import select
from utils.database import database
from models.channel import Channel
from schemas.channel import SchemasChannel, MyChannelResp, ChannelResp
from schemas.user import SchemasUser
from sqlalchemy.ext.asyncio import AsyncSession
from routers.auth import get_current_active_user
from functions.channel import (
    create_channel,
    create_photo,
    create_photo_banner,
    update_channel,
    update_profile_image,
    update_banner_image,
)


channel_router = APIRouter()


@channel_router.post("/channel")
async def kanal_yaratish(
    form: SchemasChannel,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    await create_channel(form, db, current_user)
    return {"message": "Kanal yaratildi."}


@channel_router.post("/profile_image")
async def rasim_yuklash_profilga(
    image: UploadFile,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    await create_photo(image, db, current_user)
    return {"message": "Rasim yuklandi"}


@channel_router.post("/banner_image")
async def rasim_yuklash_bannerga(
    image: UploadFile,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    await create_photo_banner(image, db, current_user)
    return {"message": "Rasim yuklandi"}


@channel_router.get("/my_channel", response_model=MyChannelResp)
async def kanal_korish(
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):

    user = await db.execute(select(Channel).where(Channel.user_id == current_user.id))
    result = user.scalar()

    if not result:
        raise HTTPException(404, "Kanal topilmadi")

    return {
        "id": result.id,
        "user_id": result.user_id,
        "channel_name": result.name,
        "channel_description": result.description,
        "profile_image": result.profile_image,
        "banner_image": result.banner_image,
        "created_at": result.created_at,
        "subscription_amount": result.subscription_amount,
    }


@channel_router.get("/channel", response_model=List[ChannelResp])
async def kanalni_korish_barchaga(
    response: Response,
    search: Optional[str] = None,
    db: AsyncSession = Depends(database),
):

    query = select(Channel)
    if search:
        query = query.where(Channel.name.ilike(f"%{search}%"))

    result = await db.execute(query)
    channels = result.scalars().all()

    response.headers["Cache-Control"] = "public, max-age=600"

    return [
        ChannelResp(
            id=ch.id,
            channel_name=ch.name,
            channel_description=ch.description,
            profile_image=ch.profile_image,
            banner_image=ch.banner_image,
            created_at=ch.created_at,
            subscription_amount=ch.subscription_amount,
        )
        for ch in channels
    ]


@channel_router.put("/channel")
async def kanal_tahrirlash(
    form: SchemasChannel,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    await update_channel(form, db, current_user)
    return {"message": "Kanal tahrirlandi."}


@channel_router.put("/profile_image")
async def rasim_tahrirlash_profile(
    image: UploadFile,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):

    await update_profile_image(image, db, current_user)
    return {"message": "Rasim tahrirlandi."}


@channel_router.put("/banner_image")
async def rasim_tahrirlash_banner(
    image: UploadFile,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):

    await update_banner_image(image, db, current_user)
    return {"message": "Rasim tahrirlandi."}


@channel_router.delete("/channel")
async def kanal_ochirish(
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    await db.execute(delete(Channel).where(Channel.user_id == current_user.id))
    await db.commit()
    return {"message": "Kanal ochirildi."}

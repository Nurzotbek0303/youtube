from fastapi import APIRouter, Depends, UploadFile, HTTPException
from sqlalchemy import delete

from sqlalchemy.future import select
from utils.database import database
from models.channel import Channel
from schemas.channel import SchemasChannel
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


@channel_router.post("/post_channel")
async def kanal_yaratish(
    form: SchemasChannel,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    try:
        await create_channel(form, db, current_user)
        return {"message": "Kanal yaratildi."}

    except Exception as err:
        return {"message": "Xatolik bor!", "Error": str(err)}


@channel_router.post("/post_profile_image")
async def rasim_yuklash_profilga(
    image: UploadFile,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    try:
        await create_photo(image, db, current_user)
        return {"message": "Rasim yuklandi"}

    except Exception as err:
        return {"message": "Xatolik bor!", "Error": str(err)}


@channel_router.post("/post_banner_image")
async def rasim_yuklash_bannerga(
    image: UploadFile,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    try:
        await create_photo_banner(image, db, current_user)
        return {"message": "Rasim yuklandi"}

    except Exception as err:
        return {"message": "Xatolik bor!", "Error": str(err)}


@channel_router.get("/my_channel")
async def kanal_korish(
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    try:
        user = await db.execute(
            select(Channel).where(Channel.user_id == current_user.id)
        )
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

    except Exception as err:
        return {"message": "Xatolik bor!", "Error": str(err)}


@channel_router.get("/get_channel")
async def kanalni_korish_barchaga(
    name: str = None, db: AsyncSession = Depends(database)
):
    try:
        if name is None:
            result = await db.execute(select(Channel))
            channels = result.scalars().all()
            return [
                {
                    "id": row.id,
                    "user_id": row.user_id,
                    "channel_name": row.name,
                    "channel_description": row.description,
                    "profile_image": row.profile_image,
                    "banner_image": row.banner_image,
                    "created_at": row.created_at,
                    "subscription_amount": row.subscription_amount,
                }
                for row in channels
            ]

        channel = await db.execute(select(Channel).where(Channel.name == name))
        result = channel.scalar_one_or_none()

        if not result:
            raise HTTPException(404, "Bunday kanal mavjud emas.")

        return {
            "id": result.id,
            "channel_name": result.name,
            "channel_description": result.description,
            "profile_image": result.profile_image,
            "banner_image": result.banner_image,
            "created_at": result.created_at,
            "subscription_amount": result.subscription_amount,
        }

    except Exception as err:
        return {"message": "Xatolik bor!", "Error": str(err)}


@channel_router.put("/put_channel")
async def kanal_tahrirlash(
    form: SchemasChannel,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    try:
        await update_channel(form, db, current_user)
        return {"message": "Kanal tahrirlandi."}

    except Exception as err:
        return {"message": "Xatolik bor!", "Error": str(err)}


@channel_router.put("/put_profile_image")
async def rasim_tahrirlash_prifile(
    image: UploadFile,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    try:
        await update_profile_image(image, db, current_user)
        return {"message": "Rasim tahrirlandi."}

    except Exception as err:
        return {"message": "Xatolik bor!", "Error": str(err)}


@channel_router.put("/put_banner_image")
async def rasim_tahrirlash_banner(
    image: UploadFile,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    try:
        await update_banner_image(image, db, current_user)
        return {"message": "Rasim tahrirlandi."}

    except Exception as err:
        return {"message": "Xatolik bor!", "Error": str(err)}


@channel_router.delete("/delete_channel")
async def kanal_ochirish(
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    try:
        await db.execute(delete(Channel).where(Channel.user_id == current_user.id))
        await db.commit()
        return {"message": "Kanal ochirildi."}

    except Exception as err:
        return {"message": "Xatolik bor!", "Error": str(err)}

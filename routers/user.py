from fastapi import APIRouter, Depends, UploadFile, HTTPException
from sqlalchemy import delete

from sqlalchemy.future import select
from utils.database import database
from models.user import User
from schemas.user import SchemasUser, UserResp
from sqlalchemy.ext.asyncio import AsyncSession
from routers.auth import get_current_active_user
from functions.user import create_user, create_photo, update_user, update_photo

user_router = APIRouter()


@user_router.post("/users")
async def royxatdan_otish(form: SchemasUser, db: AsyncSession = Depends(database)):

    await create_user(form, db)
    return {"message": "Foydananuvchi qoshildi."}


@user_router.post("/users/photo")
async def rasim_yuklash(
    image: UploadFile,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    await create_photo(image, db, current_user)
    return {"message": "Rasim yuklandi."}


@user_router.get("/users/me", response_model=UserResp)
async def royxad_korish(
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    user = await db.execute(select(User).where(User.email == current_user.email))
    result = user.scalar()

    if not result:
        raise HTTPException(404, "Foydalanuvchi topilmadi")

    return {
        "id": result.id,
        "username": result.username,
        "email": result.email,
        "create_at": result.create_at,
        "user_image": result.image,
    }


@user_router.put("/users/me")
async def royxad_tahrirlash(
    form: SchemasUser,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    await update_user(form, db, current_user)
    return {"message": "Foydalanuvchi tahrirlandi."}


@user_router.put("/users/update")
async def rasim_tahrirlash(
    image: UploadFile,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    await update_photo(image, db, current_user)
    return {"message": "Rasim tahrirlandi."}


@user_router.delete("/users/me")
async def foydalanuvchi_ochirish(
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    await db.execute(delete(User).where(User.id == current_user.id))
    await db.commit()
    return {"message": "Foydalanuvchi ochirildi."}

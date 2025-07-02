from fastapi import APIRouter, Depends, UploadFile, HTTPException
from sqlalchemy import delete

from sqlalchemy.future import select
from utils.database import database
from models.user import User
from schemas.user import SchemasUser
from sqlalchemy.ext.asyncio import AsyncSession
from routers.auth import get_current_active_user
from functions.user import create_user, create_photo, update_user, update_photo

user_router = APIRouter()


@user_router.post("/post_user")
async def royxatdan_otish(form: SchemasUser, db: AsyncSession = Depends(database)):
    try:
        await create_user(form, db)
        return {"message": "Foydananuvchi qoshildi."}
    except Exception as err:
        return {"message": "Xatolik bor!", "Error": str(err)}


@user_router.post("/post_image")
async def rasim_yuklash(
    image: UploadFile,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    try:
        await create_photo(image, db, current_user)
        return {"message": "Rasim yuklandi."}

    except Exception as err:
        return {"message": "Xatolik bor!", "Error": str(err)}


@user_router.get("/get_user")
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
        "password": result.password,
        "create_at": result.create_at,
        "user_image": result.image,
    }


@user_router.put("/put_user")
async def royxad_tahrirlash(
    form: SchemasUser,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    try:
        await update_user(form, db, current_user)
        return {"message": "Foydalanuvchi tahrirlandi."}

    except Exception as err:
        return {"message": "Xatolik bor!", "Error": str(err)}


@user_router.put("/put_image")
async def rasim_tahrirlash(
    image: UploadFile,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    try:
        await update_photo(image, db, current_user)
        return {"message": "Rasim tahrirlandi."}

    except Exception as err:
        return {"message": "Xatolik bor!", "Error": str(err)}


@user_router.delete("/delete_user")
async def foydalanuvchi_ochirish(
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    try:
        await db.execute(delete(User).where(User.id == current_user.id))
        await db.commit()
        return {"message": "Foydalanuvchi ochirildi."}

    except Exception as err:
        return {"message": "Xatolik bor!", "Error": str(err)}

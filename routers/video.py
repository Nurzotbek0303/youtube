from fastapi import APIRouter, Depends, UploadFile, HTTPException, File

from sqlalchemy import update, delete, literal_column
from sqlalchemy.future import select
from utils.database import database
from models.video import Video
from models.channel import Channel
from schemas.user import SchemasUser
from schemas.video import SchemasVideo, VidyoResponse, UpdateVideo, Category
from sqlalchemy.ext.asyncio import AsyncSession
from routers.auth import get_current_active_user
from functions.video import create_vidyo, update_video


video_router = APIRouter()


@video_router.post("/post_video")
async def video_qoshish(
    form: SchemasVideo = Depends(SchemasVideo.as_form),
    vidyo: UploadFile = File(...),
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    try:
        await create_vidyo(form, vidyo, db, current_user)
        return {"message": "Video yuklandi."}

    except Exception as err:
        return {"message": "Xatolik bor!", "Error": str(err)}


@video_router.get("/my_video")
async def meni_videolarim(
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    try:
        result = await db.execute(
            select(
                Video.id,
                Channel.name.label("name"),
                Channel.profile_image.label("profile_image"),
                Video.title,
                Video.description,
                Video.file_path,
                Video.thumbnail_path,
                Video.category,
                Video.views,
                Video.created_at,
                Video.like_amount,
            )
            .select_from(Video)
            .join(Channel, Channel.id == Video.channel_id)
            .where(Channel.user_id == current_user.id)
        )

        rows = result.all()
        if not rows:
            raise HTTPException(404, "Video topilmadi.")

        return [VidyoResponse(**row._mapping) for row in rows]

    except Exception as err:
        return {"message": "Xatolik bor!", "Error": str(err)}


@video_router.get("/get_video")
async def videolar_korish(
    ident: int = None, category: Category = None, db: AsyncSession = Depends(database)
):
    try:
        if ident:
            video_check = await db.execute(select(Video.id).where(Video.id == ident))
            if not video_check.scalar():
                raise HTTPException(404, "Bunday video mavjud emas.")

            await db.execute(
                update(Video)
                .where(Video.id == ident)
                .values(views=literal_column("views") + 1)
            )
            await db.commit()

        query = (
            select(
                Video.id,
                Channel.name.label("name"),
                Channel.profile_image.label("profile_image"),
                Video.title,
                Video.description,
                Video.file_path,
                Video.thumbnail_path,
                Video.category,
                Video.views.label("views"),
                Video.created_at,
                Video.like_amount,
            )
            .select_from(Video)
            .join(Channel, Channel.id == Video.channel_id)
        )

        if ident:
            query = query.filter(Video.id == ident)
        if category:
            query = query.filter(Video.category == category)

        result = await db.execute(query)

        if ident:
            row = result.first()
            if not row:
                raise HTTPException(404, "Video topilmadi.")
            return VidyoResponse(**row._mapping)

        rows = result.all()
        return [VidyoResponse(**row._mapping) for row in rows]

    except Exception as err:
        return {"message": "Xatolik bor!", "Error": str(err)}


@video_router.put("/put_video")
async def video_tahrirlash(
    form: UpdateVideo,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    try:
        await update_video(form, db, current_user)
        return {"message": "Video tahrirlasndi."}

    except Exception as err:
        return {"message": "Xatolik bor!", "Error": str(err)}


@video_router.delete("/delete_video")
async def video_ochirish(
    video_id: int,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    try:
        kanal = await db.execute(
            select(Channel).where(Channel.user_id == current_user.id)
        )
        kanal_result = kanal.scalar()

        if not kanal_result:
            raise HTTPException(404, "Sizning kanal topilmadi.")

        video = await db.execute(
            select(Video).where(
                Video.id == video_id, Video.channel_id == kanal_result.id
            )
        )
        result = video.scalar()

        if not result:
            raise HTTPException(
                404, "Bunday video sizga tegishli emas yoki mavjud emas."
            )

        await db.execute(delete(Video).where(Video.id == video_id))
        await db.commit()
        return {"message": "Video ochirildi."}

    except Exception as err:
        return {"message": "Xatolik bor!", "Error": str(err)}

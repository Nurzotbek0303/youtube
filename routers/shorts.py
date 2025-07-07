from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy import update, delete

from models.shorts import Shorts
from models.channel import Channel
from schemas.user import SchemasUser
from utils.database import database
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from routers.auth import get_current_active_user
from functions.shorts import create_shorts

shorts_router = APIRouter()


@shorts_router.post("/post_shorts")
async def shorts_vidyo_qoshish(
    video: UploadFile = File(...),
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    try:
        await create_shorts(video, db, current_user)
        return {"message": "Shorts qoshildi."}

    except Exception as err:
        return {"message": "Xatolik bor!", "Error": str(err)}


@shorts_router.get("/get_shorts")
async def shorts_vidyo_korish(ident: int, db: AsyncSession = Depends(database)):
    try:
        query = await db.execute(select(Shorts).where(Shorts.id == ident))
        result = query.scalar_one_or_none()
        if not result:
            raise HTTPException(404, "Shorts topilmadi")

        await db.execute(
            update(Shorts).where(Shorts.id == ident).values(views=result.views + 1)
        )
        await db.commit()

        full_query = await db.execute(
            select(
                Shorts.id,
                Shorts.video_url,
                Shorts.thumbnail_path,
                Channel.name.label("channel_name"),
                Channel.profile_image,
                Shorts.like_amount,
                Shorts.views,
                Shorts.created_at,
            )
            .select_from(Shorts)
            .join(Channel, Channel.id == Shorts.channel_id)
            .where(Shorts.id == ident)
        )
        row = full_query.first()

        if not row:
            raise HTTPException(404, "Ma'lumot topilmadi")

        return {
            "id": row.id,
            "video_url": row.video_url,
            "thumbnail_path": row.thumbnail_path,
            "channel_name": row.channel_name,
            "profile_image": row.profile_image,
            "like_amount": row.like_amount,
            "views": row.views,
            "created_at": row.created_at,
        }

    except Exception as err:
        return {"message": "Xatolik bor!", "Error": str(err)}


@shorts_router.delete("/delete_shorts")
async def shorts_ochirish(
    ident: int,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    try:
        channel_result = await db.execute(
            select(Channel).where(Channel.user_id == current_user.id)
        )
        user_channel = channel_result.scalar()

        if not user_channel:
            raise HTTPException(400, "Sizda kanal mavjud emas.")

        shorts_result = await db.execute(
            select(Shorts).where(
                Shorts.id == ident,
                Shorts.channel_id == user_channel.id,
            )
        )
        shorts = shorts_result.scalar()

        if not shorts:
            raise HTTPException(
                404,
                "Sizda ushbu ID raqamli video mavjud emas yoki sizga tegishli emas.",
            )

        await db.execute(delete(Shorts).where(Shorts.id == ident))
        await db.commit()
        return {"message": "Shorts muvaffaqiyatli o'chirildi."}

    except Exception as err:
        return {"message": "Xatolik bor!", "Error": str(err)}

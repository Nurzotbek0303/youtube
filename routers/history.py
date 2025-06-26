from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete

from models.history import History
from models.channel import Channel
from models.video import Video
from models.user import User
from schemas.user import SchemasUser
from schemas.history import SchemasHistory, HistoryResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from utils.database import database
from routers.auth import get_current_active_user
from functions.history import cretae_history
from utils.check import check_history


history_router = APIRouter()


@history_router.post("/post_histor")
async def tarix_qoshish(
    form: SchemasHistory,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    try:
        await cretae_history(form, db, current_user)
        return {"message": "History qoshildi."}

    except Exception as err:
        return {"message": "Xatolik bor!", "Error": str(err)}


@history_router.get("/get_history")
async def tomosha_tarixi(
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    try:
        query = (
            select(
                History.id,
                User.username,
                Channel.name.label("name"),
                Video.title,
                Video.file_path,
                Video.thumbnail_path,
                Video.views,
                History.watched_at,
            )
            .join(User, User.id == History.user_id)
            .join(Video, Video.id == History.video_id)
            .join(Channel, Channel.id == Video.channel_id)
            .where(History.user_id == current_user.id)
            .order_by(History.watched_at.desc())
        )

        result = await db.execute(query)
        rows = result.all()

        if not rows:
            raise HTTPException(404, detail="Tarix topilmadi.")

        return [HistoryResponse(**row._mapping) for row in rows]

    except Exception as err:
        return {"message": "Xatolik bor!", "Error": str(err)}


@history_router.delete("/delete_history")
async def tarixni_tozalash(
    ident: int,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    try:
        await check_history(db, ident, History, current_user)

        await db.execute(delete(History).where(History.id == ident))
        await db.commit()
        return {"message": "Tarix muvaffaqiyatli o'chirildi."}

    except Exception as err:
        return {"message": "Xatolik yuz berdi", "error": str(err)}

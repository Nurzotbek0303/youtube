from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete
from typing import List, Union

from models.history import History
from models.channel import Channel
from models.video import Video
from models.user import User
from schemas.user import SchemasUser
from schemas.history import SchemasHistory, HistoryResp
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from utils.database import database
from routers.auth import get_current_active_user
from functions.history import cretae_history
from utils.check import check_history


history_router = APIRouter()


@history_router.post("{video_id:int}")
async def tarix_qoshish(
    form: SchemasHistory,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    await cretae_history(form, db, current_user)
    return {"message": "History qoshildi."}


@history_router.get("", response_model=Union[List[HistoryResp], dict])
async def tomosha_tarixi(
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    query = (
        select(
            History.id,
            Channel.name.label("channel_name"),
            Video.title,
            Video.thumbnail_path,
            Video.description,
            Video.id.label("video_id"),
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

    return [
        {
            "id": row.id,
            "channel_name": row.channel_name,
            "video_title": row.title,
            "thumbnail_path": row.thumbnail_path,
            "video_description": row.description,
            "video_id": row.video_id,
            "views": row.views,
            "watched_at": row.watched_at,
        }
        for row in rows
    ]


@history_router.delete("{ident:int}")
async def tarixni_tozalash(
    ident: int,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    await check_history(db, ident, History, current_user)

    await db.execute(delete(History).where(History.id == ident))
    await db.commit()
    return {"message": "Tarix muvaffaqiyatli o'chirildi."}

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from sqlalchemy import update, delete
from typing import List, Union

from models.shorts import Shorts
from models.channel import Channel
from schemas.user import SchemasUser
from schemas.shorts import ShortsResp
from utils.database import database
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from routers.auth import get_current_active_user
from functions.shorts import create_shorts

shorts_router = APIRouter()


@shorts_router.post("")
async def shorts_vidyo_qoshish(
    video: UploadFile = File(...),
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    await create_shorts(video, db, current_user)
    return {"message": "Shorts qoshildi."}


@shorts_router.get("/page", response_model=List[ShortsResp])
async def get_shorts_list(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    sort_by: str = Query("created_at", regex="^(created_at|views|like_amount)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    db: AsyncSession = Depends(database),
):
    query = (
        select(
            Shorts.id,
            Channel.name.label("channel_name"),
            Channel.profile_image,
            Shorts.video_url,
            Shorts.thumbnail_path,
            Shorts.views,
            Shorts.created_at,
            Shorts.like_amount,
        )
        .select_from(Shorts)
        .join(Channel, Channel.id == Shorts.channel_id)
    )

    if sort_by == "created_at":
        order_column = Shorts.created_at
    elif sort_by == "views":
        order_column = Shorts.views
    elif sort_by == "like_amount":
        order_column = Shorts.like_amount
    else:
        order_column = Shorts.created_at

    if sort_order == "desc":
        query = query.order_by(order_column.desc())
    else:
        query = query.order_by(order_column.asc())

    query = query.offset((page - 1) * limit).limit(limit)

    result = await db.execute(query)
    rows = result.all()

    return [
        {
            "id": row.id,
            "channel_name": row.channel_name,
            "profile_image": row.profile_image,
            "video_url": row.video_url,
            "thumbnail_path": row.thumbnail_path,
            "views": row.views,
            "created_at": row.created_at,
            "like_amount": row.like_amount,
        }
        for row in rows
    ]


@shorts_router.get("", response_model=Union[List[ShortsResp], ShortsResp])
async def shorts_vidyo_korish(db: AsyncSession = Depends(database)):

    query_shorts = await db.execute(
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
    )
    rows = query_shorts.all()
    return [
        {
            "id": row.id,
            "video_url": row.video_url,
            "thumbnail_path": row.thumbnail_path,
            "channel_name": row.channel_name,
            "profile_image": row.profile_image,
            "like_amount": row.like_amount,
            "views": row.views,
            "created_at": row.created_at,
        }
        for row in rows
    ]


@shorts_router.delete("{ident}")
async def shorts_ochirish(
    ident: int,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):

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

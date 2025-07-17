from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete
from typing import List

from utils.database import database
from sqlalchemy.future import select
from models.user import User
from models.shorts import Shorts
from models.shorts_like import ShortsLike
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import SchemasUser
from schemas.shorts_like import SchemasShortsLike, ShortsLikeResp
from routers.auth import get_current_active_user
from functions.shorts_like import create_shortsLike

shorts_like_router = APIRouter()


@shorts_like_router.post("")
async def shorts_like(
    form: SchemasShortsLike,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):

    await create_shortsLike(form, db, current_user)
    return {"message": "Shorts like qoshildi."}


@shorts_like_router.get("", response_model=List[ShortsLikeResp])
async def shorts_like_korish(
    ident: int = None,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    result = (
        (
            await db.execute(
                select(ShortsLike).where(ShortsLike.user_id == current_user.id)
            )
        )
        .scalars()
        .all()
    )

    if not result:
        raise HTTPException(404, "Siz hech qanday shortsga like bosmagansiz.")

    if ident is None:
        query = await db.execute(
            select(
                ShortsLike.id,
                User.username,
                Shorts.id.label("shorts_id"),
                Shorts.video_url,
                ShortsLike.is_like,
                ShortsLike.created_at,
            )
            .select_from(ShortsLike)
            .join(User, User.id == ShortsLike.user_id)
            .join(Shorts, Shorts.id == ShortsLike.video_id)
            .where(ShortsLike.user_id == current_user.id)
        )
        rows = query.all()

        return [
            {
                "id": row.id,
                "username": row.username,
                "shorts_id": row.shorts_id,
                "video_url": row.video_url,
                "is_like": row.is_like,
                "created_at": row.created_at,
            }
            for row in rows
        ]

    query = await db.execute(
        select(
            ShortsLike.id,
            User.username,
            Shorts.id.label("shorts_id"),
            Shorts.video_url,
            ShortsLike.is_like,
            ShortsLike.created_at,
        )
        .select_from(ShortsLike)
        .join(User, User.id == ShortsLike.user_id)
        .join(Shorts, Shorts.id == ShortsLike.video_id)
        .where(ShortsLike.id == ident, ShortsLike.user_id == current_user.id)
    )
    row = query.first()

    if not row:
        raise HTTPException(404, "Bunday shorts like topilmadi.")

    return {
        "id": row.id,
        "username": row.username,
        "shorts_id": row.shorts_id,
        "video_url": row.video_url,
        "is_like": row.is_like,
        "created_at": row.created_at,
    }


@shorts_like_router.delete("")
async def shorts_like_ochirish(
    ident: int,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):

    shorts = await db.execute(
        select(ShortsLike).where(ShortsLike.user_id == current_user.id)
    )
    result = shorts.scalar()
    if not result:
        shorts_first = await db.execute(
            select(ShortsLike).where(ShortsLike.id == ident)
        )
        result_first = shorts_first.scalar()
        if result_first:
            if result.is_like:
                result_first.like_amount = max(result_first.like_amount - 1, 0)
            else:
                result_first.dislike_amount = max(result_first.dislike_amount - 1, 0)

            db.add(result_first)
            await db.execute(delete(ShortsLike).where(ShortsLike.id == ident))
        await db.commit()
        return {"message": "Like o'chirildi."}

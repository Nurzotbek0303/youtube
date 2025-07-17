from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import update, delete
from typing import List

from schemas.shorts_comment import SchemasShortsComment, ShortsCommentResp
from schemas.user import SchemasUser
from sqlalchemy.future import select
from utils.database import database
from models.shorts import Shorts
from models.channel import Channel
from models.shorts_comment import ShortsComment
from sqlalchemy.ext.asyncio import AsyncSession
from routers.user import SchemasUser
from routers.auth import get_current_active_user
from functions.shorts_comment import create_shorts_comment, update_shortsComment

shorts_commment_router = APIRouter()


@shorts_commment_router.post("")
async def shorts_comment_yozish(
    form: SchemasShortsComment,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    await create_shorts_comment(form, db, current_user)
    return {"message": "Shorts comment yozildi."}


@shorts_commment_router.get("", response_model=List[ShortsCommentResp])
async def shorts_comment(shorts_id: int, db: AsyncSession = Depends(database)):
    shorts = await db.execute(select(Shorts).where(Shorts.id == shorts_id))
    result = shorts.scalar()
    if not result:
        raise HTTPException(404, "Bunday shorts video mavjud emas.")
    query = (
        select(
            Shorts.id,
            ShortsComment.comment,
            Channel.name,
            ShortsComment.id.label("shortsComent_id"),
            ShortsComment.created_at,
        )
        .join(ShortsComment, ShortsComment.video_id == Shorts.id)
        .join(Channel, Channel.id == Shorts.channel_id)
        .where(Shorts.id == shorts_id)
    )
    result_video = await db.execute(query)
    rows = result_video.all()

    return [
        {
            "id": row.id,
            "comment": row.comment,
            "channel_name": row.name,
            "shortsComent_id": row.shortsComent_id,
            "created_at": row.created_at,
        }
        for row in rows
    ]


@shorts_commment_router.put("")
async def shorts_comment_tahrirlash(
    ident: int,
    form: SchemasShortsComment,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):

    update_shortsComment(ident, form, db, current_user)
    return {"message": "Shorts comment tahrirlandi."}


@shorts_commment_router.delete("")
async def shorts_comment_ochirish(
    ident: int,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):

    shorts = await db.execute(
        select(ShortsComment.id == ident, ShortsComment.user_id == current_user.id)
    )
    result = shorts.scalar()
    if not result:
        raise HTTPException(404, "Bunday shorts id mavjud emas.")

    await db.execute(delete(ShortsComment).where(ShortsComment.id == ident))
    await db.commit()
    return {"message": "Izoh ochirildi."}

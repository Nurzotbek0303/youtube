from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete

from models.comment import Comment
from schemas.user import SchemasUser
from schemas.comment import SchemasComment
from utils.database import database
from sqlalchemy.ext.asyncio import AsyncSession
from routers.auth import get_current_active_user
from functions.comment import create_comment, update_comment
from utils.check import check_comment_user

comment_router = APIRouter()


@comment_router.post("")
async def izoh_yozish(
    form: SchemasComment,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    await create_comment(form, db, current_user)
    return {"message": "Izoh yozildi."}


@comment_router.put("")
async def izoh_tahrirlash(
    ident: int,
    form: SchemasComment,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    await update_comment(ident, form, db, current_user)
    return {"message": "Izoh tahrirlandi."}


@comment_router.delete("")
async def izoh_ochirish(
    comment_id: str,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    await check_comment_user(db, comment_id, Comment, current_user)
    await db.execute(delete(Comment).where(Comment.id == comment_id))
    await db.commit()
    return {"message": "Izoh ochirildi."}

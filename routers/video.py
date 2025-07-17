from fastapi import APIRouter, Depends, UploadFile, HTTPException, File, Query, Response
from typing import List, Union, Optional

from sqlalchemy import update, delete, literal_column
from sqlalchemy.future import select
from utils.database import database
from models.video import Video
from models.channel import Channel
from schemas.user import SchemasUser, UserResp
from models.comment import Comment
from schemas.video import (
    SchemasVideo,
    UpdateVideo,
    Category,
    MyVideoResp,
    VideoResp,
    CommentResp,
)
from sqlalchemy.ext.asyncio import AsyncSession
from routers.auth import get_current_active_user
from functions.video import create_vidyo, update_video


video_router = APIRouter()


@video_router.post("/video")
async def video_qoshish(
    form: SchemasVideo = Depends(SchemasVideo.as_form),
    vidyo: UploadFile = File(...),
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    await create_vidyo(form, vidyo, db, current_user)
    return {"message": "Video yuklandi."}


# shu yerga kash qoshildi
@video_router.get("/videos", response_model=List[VideoResp])
async def get_videos(
    response: Response,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = Query("created_at", regex="^(created_at|views|like_amount|title)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    db: AsyncSession = Depends(database),
):
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
            Video.views,
            Video.created_at,
            Video.like_amount,
            Video.duration_video,
        )
        .select_from(Video)
        .join(Channel, Channel.id == Video.channel_id)
    )

    if category:
        query = query.filter(Video.category == category)

    if search:
        query = query.filter(
            Video.title.contains(search) | Video.description.contains(search)
        )

    if sort_by == "created_at":
        order_column = Video.created_at
    elif sort_by == "views":
        order_column = Video.views
    elif sort_by == "like_amount":
        order_column = Video.like_amount
    elif sort_by == "title":
        order_column = Video.title
    else:
        order_column = Video.created_at

    if sort_order == "desc":
        query = query.order_by(order_column.desc())
    else:
        query = query.order_by(order_column.asc())

    query = query.offset((page - 1) * limit).limit(limit)

    result = await db.execute(query)
    rows = result.all()

    response.headers["Cache-Control"] = "public, max-age=600"

    return [
        {
            "id": row.id,
            "channel_name": row.name,
            "profile_image": row.profile_image,
            "video_title": row.title,
            "video_description": row.description,
            "file_path": row.file_path,
            "thumbnail_path": row.thumbnail_path,
            "category": row.category,
            "video_views": row.views,
            "created_at": row.created_at,
            "like_amount": row.like_amount,
            "duration_video": row.duration_video,
        }
        for row in rows
    ]


@video_router.get("/videos/{video_id}", response_model=VideoResp)
async def videolar(video_id: int, db: AsyncSession = Depends(database)):
    query = await db.execute(select(Video.id).where(Video.id == video_id))
    return query


@video_router.get("/my/video", response_model=List[MyVideoResp])
async def mening_videolarim(
    response: Response,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
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
            Video.duration_video,
            Video.dislike_amount,
        )
        .select_from(Video)
        .join(Channel, Channel.id == Video.channel_id)
        .where(Channel.user_id == current_user.id)
    )

    rows = result.all()
    if not rows:
        raise HTTPException(404, "Video topilmadi.")

    response.headers["Cache-Control"] = "public, max-age=600"

    return [
        {
            "id": row.id,
            "name": row.name,
            "profile_image": row.profile_image,
            "title": row.title,
            "description": row.description,
            "file_path": row.file_path,
            "thumbnail_path": row.thumbnail_path,
            "category": row.category,
            "views": row.views,
            "created_at": row.created_at,
            "like_amount": row.like_amount,
            "duration_video": row.duration_video,
            "dislike_amount": row.dislike_amount,
        }
        for row in rows
    ]


@video_router.get("/video", response_model=Union[List[VideoResp], VideoResp])
async def videolar_korish(
    response: Response,
    ident: int = None,
    category: Category = None,
    db: AsyncSession = Depends(database),
):
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
            Video.duration_video,
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
        return {
            "id": row.id,
            "channel_name": row.name,
            "profile_image": row.profile_image,
            "video_title": row.title,
            "video_description": row.description,
            "file_path": row.file_path,
            "thumbnail_path": row.thumbnail_path,
            "category": row.category,
            "video_views": row.views,
            "created_at": row.created_at,
            "like_amount": row.like_amount,
            "duration_video": row.duration_video,
        }

    rows = result.all()

    response.headers["Cache-Control"] = "public, max-age=600"
    return [
        {
            "id": data.id,
            "channel_name": data.name,
            "profile_image": data.profile_image,
            "video_title": data.title,
            "video_description": data.description,
            "file_path": data.file_path,
            "thumbnail_path": data.thumbnail_path,
            "category": data.category,
            "video_views": data.views,
            "created_at": data.created_at,
            "like_amount": data.like_amount,
            "duration_video": data.duration_video,
        }
        for data in rows
    ]


@video_router.get("/video/comment", response_model=List[CommentResp])
async def video_comment_korish(
    response: Response, video_id: int, db: AsyncSession = Depends(database)
):

    video = await db.execute(select(Video).where(Video.id == video_id))
    result = video.scalar()
    if not result:
        raise HTTPException(404, "Bunday video mavjud emas.")

    query = (
        select(
            Video.id.label("video_id"),
            Comment.comment,
            Channel.name.label("channel_name"),
            Comment.id.label("comment_id"),
            Comment.created_at,
        )
        .join(Comment, Comment.video_id == Video.id)
        .join(Channel, Channel.id == Video.channel_id)
        .where(Video.id == video_id)
    )

    result_video = await db.execute(query)
    rows = result_video.all()
    response.headers["Cache-Control"] = "public, max-age=600"
    return [
        {
            "id": row.video_id,
            "comment": row.comment,
            "channel_name": row.channel_name,
            "comment_id": row.comment_id,
            "created_at": row.created_at,
        }
        for row in rows
    ]


@video_router.put("/video")
async def video_tahrirlash(
    ident: int,
    form: UpdateVideo,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    await update_video(ident, form, db, current_user)
    return {"message": "Video tahrirlasndi."}


@video_router.delete("/video")
async def video_ochirish(
    video_id: int,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    kanal = await db.execute(select(Channel).where(Channel.user_id == current_user.id))
    kanal_result = kanal.scalar()

    if not kanal_result:
        raise HTTPException(404, "Sizning kanal topilmadi.")

    video = await db.execute(
        select(Video).where(Video.id == video_id, Video.channel_id == kanal_result.id)
    )
    result = video.scalar()

    if not result:
        raise HTTPException(404, "Bunday video sizga tegishli emas yoki mavjud emas.")

    await db.execute(delete(Video).where(Video.id == video_id))
    await db.commit()
    return {"message": "Video ochirildi."}

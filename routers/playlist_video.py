from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import update, delete

from utils.database import database
from models.playlist_video import PlaylistVideo
from models.video import Video
from models.playlist import Playlist
from models.channel import Channel
from schemas.playlist_video import SchemasPlaylistVideo
from schemas.user import SchemasUser
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from routers.auth import get_current_active_user
from functions.playlist_video import create_playlist_video

playlist_video_router = APIRouter()


@playlist_video_router.post("post_playlist_video")
async def playlist_video_qoshish(
    form: SchemasPlaylistVideo,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    try:
        await create_playlist_video(form, db, current_user)
        return {"message": "Video yuklandi."}

    except Exception as err:
        return {"message": "Xatolik bor!", "Error": str(err)}


@playlist_video_router.get("/my_playlist_video")
async def playlist_videoni_korish(
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    try:
        playlist_video = (
            select(
                PlaylistVideo.id,
                Video.title,
                Video.file_path,
                Playlist.is_personal,
            )
            .select_from(PlaylistVideo)
            .join(Video, Video.id == PlaylistVideo.video_id)
            .join(Playlist, Playlist.id == PlaylistVideo.playlist_id)
            .join(Channel, Channel.id == Playlist.channel_id)
            .where(Channel.user_id == current_user.id)
        )
        result = await db.execute(playlist_video)
        rows = result.all()

        return [
            {
                "id": row.id,
                "title": row.title,
                "file_path": row.file_path,
                "is_personal": row.is_personal,
            }
            for row in rows
        ]
    except Exception as err:
        return {"message": "Xatolik yuz berdi", "error": str(err)}


@playlist_video_router.get("/get_playlist_video")
async def playlist_videoni_korish_barcha_uchun(db: AsyncSession = Depends(database)):
    try:
        playlist_video = (
            select(
                PlaylistVideo.id,
                Video.title,
                Video.file_path,
                Playlist.is_personal,
            )
            .select_from(PlaylistVideo)
            .join(Video, Video.id == PlaylistVideo.video_id)
            .join(Playlist, Playlist.id == PlaylistVideo.playlist_id)
            .where(Playlist.is_personal == False)
        )
        result = await db.execute(playlist_video)
        rows = result.all()

        return [
            {
                "id": row.id,
                "title": row.title,
                "file_path": row.file_path,
                "is_personal": row.is_personal,
            }
            for row in rows
        ]
    except Exception as err:
        return {"message": "Xatolik yuz berdi", "error": str(err)}


@playlist_video_router.delete("/delete_playlist_video")
async def playlist_videoni_ochirish(
    ident: int,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    try:
        query = (
            select(PlaylistVideo)
            .join(Playlist, Playlist.id == PlaylistVideo.playlist_id)
            .join(Channel, Channel.id == Playlist.channel_id)
            .where(PlaylistVideo.id == ident, Channel.user_id == current_user.id)
        )
        result = await db.execute(query)
        video = result.scalar_one_or_none()

        if not video:
            raise HTTPException(
                404, "Sizda bunday playlist video mavjud emas yoki ruxsat yo'q."
            )

        await db.execute(delete(PlaylistVideo).where(PlaylistVideo.id == ident))
        await db.commit()
        return {"message": "Playlist video o'chirildi."}

    except Exception as err:
        return {"message": "Xatolik yuz berdi", "error": str(err)}

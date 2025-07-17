from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete
from typing import List

from models.playlist import Playlist
from models.channel import Channel
from schemas.playlist import SchemasPlaylist, PlaylistResp
from schemas.user import SchemasUser
from utils.database import database
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from functions.playlist import update_playlist, create_playlist
from routers.auth import get_current_active_user

playlist_router = APIRouter()


@playlist_router.post("")
async def playlist_yaratish(
    form: SchemasPlaylist,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    await create_playlist(form, db, current_user)
    return {"message": "Playlist yaratildi."}


@playlist_router.get("/me", response_model=List[PlaylistResp])
async def faqat_mening_playlistlarim(
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    playlist = (
        select(
            Playlist.id,
            Channel.name.label("channel_name"),
            Channel.profile_image,
            Playlist.name.label("playlist_name"),
            Playlist.is_personal,
        )
        .select_from(Playlist)
        .join(Channel, Channel.id == Playlist.channel_id)
        .where(Channel.user_id == current_user.id)
    )
    result = await db.execute(playlist)
    rows = result.all()

    return [
        {
            "id": row.id,
            "channel_name": row.channel_name,
            "playlist_name": row.playlist_name,
            "is_personal": row.is_personal,
            "image": row.profile_image,
        }
        for row in rows
    ]


@playlist_router.get("", response_model=List[PlaylistResp])
async def barcha_korishi_mumkin(db: AsyncSession = Depends(database)):
    playlist = (
        select(
            Playlist.id,
            Channel.name.label("channel_name"),
            Channel.profile_image,
            Playlist.name.label("playlist_name"),
            Playlist.is_personal,
        )
        .select_from(Playlist)
        .join(Channel, Channel.id == Playlist.channel_id)
        .where(Playlist.is_personal == False)
    )
    result = await db.execute(playlist)
    rows = result.all()

    return [
        {
            "id": row.id,
            "channel_name": row.channel_name,
            "playlist_name": row.playlist_name,
            "is_personal": row.is_personal,
            "image": row.profile_image,
        }
        for row in rows
    ]


@playlist_router.put("")
async def playlist_tahrirlash(
    playlist_id: int,
    form: SchemasPlaylist,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    await update_playlist(playlist_id, form, db, current_user)
    return {"message": "Playlist tahrirlandi."}


@playlist_router.delete("")
async def playlistni_ochirish(
    ident: int,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    query = await db.execute(
        select(Playlist)
        .join(Channel, Playlist.channel_id == Channel.id)
        .where(Playlist.id == ident, Channel.user_id == current_user.id)
    )
    result = query.scalar_one_or_none()

    if not result:
        raise HTTPException(404, "Sizda bunday playlist mavjud emas yoki ruxsat yo'q.")

    await db.execute(delete(Playlist).where(Playlist.id == ident))
    await db.commit()
    return {"message": "Playlist o'chirildi."}

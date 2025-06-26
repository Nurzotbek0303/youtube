from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete

from models.playlist import Playlist
from models.channel import Channel
from schemas.playlist import SchemasPlaylist
from schemas.user import SchemasUser
from utils.database import database
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from functions.playlist import update_playlist, create_playlist
from routers.auth import get_current_active_user

playlist_router = APIRouter()


@playlist_router.post("/post_playlist")
async def playlist_yaratish(
    form: SchemasPlaylist,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    try:
        await create_playlist(form, db, current_user)
        return {"message": "Playlist yaratildi."}

    except Exception as err:
        return {"message": "Xatolik bor!", "Error": str(err)}


@playlist_router.get("/my_playlist")
async def faqat_mening_playlistlarim(
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    try:
        playlist = (
            select(
                Playlist.id,
                Channel.name,
                Channel.profile_image,
                Playlist.name,
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
                "name": row.name,
                "is_personal": row.is_personal,
                "channel_name": row.name,
                "image": row.profile_image,
            }
            for row in rows
        ]
    except Exception as err:
        return {"message": "Xatolik yuz berdi", "error": str(err)}


@playlist_router.get("/get_playlist")
async def barcha_korishi_mumkin(db: AsyncSession = Depends(database)):
    try:
        playlist = (
            select(
                Playlist.id,
                Channel.name,
                Channel.profile_image,
                Playlist.name,
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
                "name": row.name,
                "is_personal": row.is_personal,
                "channel_name": row.name,
                "image": row.profile_image,
            }
            for row in rows
        ]
    except Exception as err:
        return {"message": "Xatolik yuz berdi", "error": str(err)}


@playlist_router.put("/put_playlist")
async def playlist_tahrirlash(
    form: SchemasPlaylist,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    try:
        await update_playlist(form, db, current_user)
        return {"message": "Playlist tahrirlandi."}

    except Exception as err:
        return {"message": "Xatolik yuz berdi", "error": str(err)}


@playlist_router.delete("/delete_playlist")
async def playlistni_ochirish(
    ident: int,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    try:
        query = await db.execute(
            select(Playlist)
            .join(Channel, Playlist.channel_id == Channel.id)
            .where(Playlist.id == ident, Channel.user_id == current_user.id)
        )
        result = query.scalar_one_or_none()

        if not result:
            raise HTTPException(
                404, "Sizda bunday playlist mavjud emas yoki ruxsat yo'q."
            )

        await db.execute(delete(Playlist).where(Playlist.id == ident))
        await db.commit()
        return {"message": "Playlist o‘chirildi."}

    except Exception as err:
        return {"message": "Xatolik yuz berdi", "error": str(err)}

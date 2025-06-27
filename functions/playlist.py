from fastapi import HTTPException
from sqlalchemy import update

from sqlalchemy.future import select
from models.playlist import Playlist
from models.channel import Channel


async def create_playlist(form, db, current_user):
    query = select(Channel).where(Channel.user_id == current_user.id)
    result = await db.execute(query)
    channel = result.scalar_one_or_none()

    if not channel:
        raise HTTPException(400, "Sizda kanal mavjud emas.")

    new_playlist = Playlist(
        name=form.name,
        is_personal=form.is_personal,
        channel_id=channel.id,
    )
    db.add(new_playlist)
    await db.commit()


async def update_playlist(playlist_id, form, db, current_user):
    query = select(Channel).where(Channel.user_id == current_user.id)
    result = await db.execute(query)
    channel = result.scalar_one_or_none()

    if not channel:
        raise HTTPException(400, "Sizda kanal mavjud emas.")

    query = select(Playlist).where(
        Playlist.id == playlist_id, Playlist.channel_id == channel.id
    )
    result = await db.execute(query)
    playlist = result.scalar_one_or_none()

    if not playlist:
        raise HTTPException(404, "Bunday playlist topilmadi yoki sizga tegishli emas.")

    await db.execute(
        update(Playlist)
        .where(Playlist.id == playlist_id)
        .values(name=form.name, is_personal=form.is_personal)
    )
    await db.commit()

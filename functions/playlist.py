from fastapi import HTTPException
from sqlalchemy import update

from sqlalchemy.future import select
from models.playlist import Playlist
from models.channel import Channel
from utils.check import check_channel


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


async def update_playlist(form, db, current_user):
    query = select(Channel).where(Channel.user_id == current_user.id)
    result = await db.execute(query)
    channel = result.scalar_one_or_none()

    if not channel:
        raise HTTPException(400, "Sizda kanal mavjud emas.")

    await check_channel(db, Channel, form)

    await db.execute(
        update(Playlist)
        .where(Playlist.id == form.id, Playlist.channel_id == channel.id)
        .values(name=form.name, is_personal=form.is_personal)
    )
    await db.commit()

from fastapi import HTTPException

from sqlalchemy.future import select
from models.video import Video
from models.playlist import Playlist
from models.playlist_video import PlaylistVideo
from utils.check import check_video


from sqlalchemy import select
from models.channel import Channel


async def create_playlist_video(form, db, current_user):
    query = (
        select(Playlist)
        .join(Channel, Playlist.channel_id == Channel.id)
        .where(Playlist.id == form.playlist_id, Channel.user_id == current_user.id)
    )
    result = await db.execute(query)
    playlist = result.scalar_one_or_none()

    if not playlist:
        raise HTTPException(403, "Siz ushbu playlistga video yuklay olmaysiz.")

    await check_video(db, Video, form)

    new_playlist_video = PlaylistVideo(
        playlist_id=form.playlist_id, video_id=form.video_id
    )
    db.add(new_playlist_video)
    await db.commit()

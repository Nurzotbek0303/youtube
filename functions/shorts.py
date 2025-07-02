from fastapi import HTTPException
from datetime import datetime, timezone

from utils.save_video import video_upload
from sqlalchemy.future import select
from models.shorts import Shorts
from models.channel import Channel


async def create_shorts(video, db, current_user):
    query = select(Channel).where(Channel.user_id == current_user.id)
    result = await db.execute(query)
    channel = result.scalar_one_or_none()

    if not channel:
        raise HTTPException(403, "Siz ushbu kanalga shorts yuklay olmaysiz.")

    video_url, thumbnail_path, duration_video = await video_upload(video)
    now = datetime.now(timezone.utc)

    new_shorts = Shorts(
        channel_id=channel.id,
        video_url=video_url,
        thumbnail_path=thumbnail_path,
        created_at=now,
    )
    db.add(new_shorts)
    await db.commit()

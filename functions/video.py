from fastapi import HTTPException
from datetime import datetime, timezone
from sqlalchemy import update
from models.video import Video
from sqlalchemy.future import select
from utils.save_video import video_upload
from models.channel import Channel
from models.video import Video
from utils.check import check_channel_video


async def create_vidyo(form, vidyo, db, current_user):
    await check_channel_video(db, Channel, current_user)

    chennel = await db.execute(
        select(Channel).where(Channel.user_id == current_user.id)
    )
    result = chennel.scalar()
    if not result:
        raise HTTPException(404, "Bunday kanal mavjud emas.")

    video_path, thumbnail_path = await video_upload(vidyo)

    now = datetime.now(timezone.utc)

    new_vidyo = Video(
        channel_id=result.id,
        title=form.title,
        description=form.description,
        file_path=video_path,
        thumbnail_path=thumbnail_path,
        category=form.category,
        created_at=now,
    )
    db.add(new_vidyo)
    await db.commit()


async def update_video(form, db, current_user):
    channel = await db.execute(
        select(Channel).where(Channel.user_id == current_user.id)
    )
    result = channel.scalar()

    if result is None:
        raise HTTPException(400, "Sizning kanal topilmadi. Avval kanal yarating.")

    video = await db.execute(select(Video).where(Video.channel_id == result.id))
    video_result = video.scalar()

    if video_result is None:
        raise HTTPException(404, "Sizning videongiz topilmadi.")

    await db.execute(
        update(Video)
        .where(Video.channel_id == result.id)
        .values(
            title=form.title,
            description=form.description,
            category=form.category,
        )
    )
    await db.commit()

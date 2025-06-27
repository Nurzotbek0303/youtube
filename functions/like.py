from datetime import datetime, timezone
from sqlalchemy import update

from models.like import Like
from models.video import Video
from utils.check import check_video, check_like


async def create_like(form, db, current_user):
    await check_like(db, Like, form, current_user)
    await check_video(db, Video, form)

    now = datetime.now(timezone.utc)

    new_like = Like(
        user_id=current_user.id,
        video_id=form.video_id,
        is_like=form.is_like,
        created_at=now,
    )
    db.add(new_like)

    if form.is_like:
        await db.execute(
            update(Video)
            .where(Video.id == form.video_id)
            .values(like_amount=Video.like_amount + 1)
        )

    await db.commit()

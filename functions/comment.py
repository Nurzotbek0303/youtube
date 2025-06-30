from datetime import datetime, timezone
from sqlalchemy import update

from sqlalchemy.future import select
from models.comment import Comment
from models.video import Video
from utils.check import check_video, check_comment


async def create_comment(form, db, current_user):
    await check_video(db, Video, form)

    now = datetime.now(timezone.utc)

    new_comment = Comment(
        user_id=current_user.id,
        video_id=form.video_id,
        comment=form.comment,
        created_at=now,
    )
    db.add(new_comment)
    await db.commit()


async def update_comment(form, db, current_user):
    await check_video(db, Video, form)

    await db.execute(
        update(Comment)
        .where(Comment.user_id == current_user.id)
        .values(
            video_id=form.video_id,
            comment=form.comment,
        )
    )
    await db.commit()

from datetime import datetime, timezone
from sqlalchemy import update

from models.video import Video
from sqlalchemy.future import select
from models.history import History
from utils.check import check_video


async def cretae_history(form, db, current_user):
    await check_video(db, Video, form)

    history_query = await db.execute(
        select(History).where(
            History.user_id == current_user.id, History.video_id == form.video_id
        )
    )
    history = history_query.scalar_one_or_none()

    now = datetime.now(timezone.utc)

    if history:
        await db.execute(
            update(History).where(History.id == history.id).values(watched_at=now)
        )
    else:
        new_history = History(
            user_id=current_user.id,
            video_id=form.video_id,
            watched_at=now,
        )
        db.add(new_history)

    await db.commit()

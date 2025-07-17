from fastapi import HTTPException
from datetime import datetime, timezone
from sqlalchemy import update

from models.shorts_comment import ShortsComment
from models.shorts import Shorts
from sqlalchemy.future import select


async def create_shorts_comment(form, db, current_user):
    shorts = await db.execute(select(Shorts).where(Shorts.id == form.video_id))
    result = shorts.scalar()
    if not result:
        raise HTTPException(404, "Bunday shorts mavjud emas.")

    now = datetime.now(timezone.utc)

    new_comment = ShortsComment(
        user_id=current_user.id,
        video_id=form.video_id,
        comment=form.comment,
        created_at=now,
    )
    db.add(new_comment)
    await db.commit()


async def update_shortsComment(ident, form, db, current_user):
    shorts_comment = await db.execute(
        select(ShortsComment.id == ident), ShortsComment.user_id == current_user.id
    )
    result_comment = shorts_comment.scalar()
    if not result_comment:
        raise HTTPException(404, "Bunday id mavjud emas.")

    await db.execute(
        update(ShortsComment)
        .where(ShortsComment.id == ident)
        .values(
            video_id=form.video_id,
            comment=form.comment,
        )
    )
    await db.commit()

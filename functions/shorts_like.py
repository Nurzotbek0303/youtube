from fastapi import HTTPException
from datetime import datetime, timezone
from sqlalchemy import update

from models.shorts_like import ShortsLike
from models.shorts import Shorts
from sqlalchemy.future import select


async def create_shortsLike(form, db, current_user):
    shorts = await db.execute(select(Shorts).where(Shorts.id == form.video_id))
    result = shorts.scalar()
    if result:
        shorts_like = await db.execute(
            select(ShortsLike).where(ShortsLike.id == current_user.id)
        )
        result_like = shorts_like.scalar()
        if not result_like:
            now = datetime.now(timezone.utc)

            new_shorts_like = ShortsLike(
                user_id=current_user.id,
                video_id=form.video_id,
                is_like=form.is_like,
                created_at=now,
            )
            db.add(new_shorts_like)

            if form.is_like:
                await db.execute(
                    update(Shorts)
                    .where(Shorts.id == form.video_id)
                    .values(like_amount=Shorts.like_amount + 1)
                )
            else:
                await db.execute(
                    update(Shorts)
                    .where(Shorts.id == form.video_id)
                    .values(dislike_amount=Shorts.dislike_amount + 1)
                )

            await db.commit()
        else:
            raise HTTPException(400, "Siz bu videoga allaqachon like bosgansiz.")
    else:
        raise HTTPException(404, "Bunday shorts id mavjud emas.")

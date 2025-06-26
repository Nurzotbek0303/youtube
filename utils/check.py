from fastapi import HTTPException
from sqlalchemy.future import select


async def check_username(db, model, form):
    username = await db.execute(select(model).where(model.username == form.username))
    result = username.scalar_one_or_none()
    if result:
        raise HTTPException(400, "Bunday username mavjud qaytadan urinib koring.")


async def check_email(db, model, form):
    email = await db.execute(select(model).where(model.email == form.email))
    result = email.scalar_one_or_none()
    if result:
        raise HTTPException(400, "Bunday email mavjud qaytadan urinib koring.")


async def check_name(db, model, form):
    name = await db.execute(select(model).where(model.name == form.name))
    result = name.scalar_one_or_none()
    if result:
        raise HTTPException(400, "Bunday name mavjud qaytadan urinib koring.")


async def check_channel(db, model, form):
    channel = await db.execute(select(model).where(model.id == form.channel_id))
    result = channel.scalar_one_or_none()
    if not result:
        raise HTTPException(400, "Bunday kanal mavjud emas.")


async def check_have_channel(db, model, form, current_user):
    subscription = await db.execute(
        select(model).where(
            model.channel_id == form.channel_id, model.subscriber_id == current_user.id
        )
    )
    result = subscription.scalar_one_or_none()
    if result:
        raise HTTPException(400, "Siz allaqachon bu kanalga obuna bo'lgansiz.")


async def check_video(db, model, form):
    video = await db.execute(select(model).where(model.id == form.video_id))
    result = video.scalar_one_or_none()
    if not result:
        raise HTTPException(404, "Bunday video mavjud emas.")


async def check_like(db, model, form, current_user):
    like = await db.execute(
        select(model).where(
            model.user_id == current_user.id, model.video_id == form.video_id
        )
    )
    result = like.scalar()
    if result:
        raise HTTPException(400, "Siz bu videoga allaqachon like bosgansiz.")


async def check_comment(db, model, form, current_user):
    like = await db.execute(
        select(model).where(
            model.user_id == current_user.id, model.video_id == form.video_id
        )
    )
    result = like.scalar()
    if result:
        raise HTTPException(400, "Siz bu videoga allaqachon izoh yozgansiz.")


async def check_channel_video(db, model, current_user):
    channel = await db.execute(select(model).where(model.user_id == current_user.id))
    result = channel.scalar()

    if result is None:
        raise HTTPException(400, "Sizning kanal topilmadi. Avval kanal yarating.")


async def check_video_title(db, model, title):
    video_title = await db.execute(select(model).where(model.title == title))
    result = video_title.scalar()
    if not result:
        raise HTTPException(404, "Bunday video mavjud emas.")


async def check_video_channel(db, video_id, model_1, model_2, current_user):
    channel = await db.execute(
        select(model_1).where(model_1.user_id == current_user.id)
    )
    chennel_result = channel.scalar()
    if not chennel_result:
        raise HTTPException(404, "Sizning kanal topilmadi.")

    video = await db.execute(
        select(model_2).where(
            model_2.id == video_id, model_2.channel_id == chennel_result.id
        )
    )
    result = video.scalar()
    if not result:
        raise HTTPException(404, "Bunday video sizga tegishli emas yoki mavjud emas.")


async def check_history(db, ident, model, current_user):
    query = select(model).where(model.id == ident, model.user_id == current_user.id)
    result = await db.execute(query)
    history = result.scalar_one_or_none()

    if not history:
        raise HTTPException(404, "Bu tarix sizga tegishli emas yoki mavjud emas.")


async def check_comment_user(db, comment_id, model, current_user):
    query = await db.execute(
        select(model).where(model.id == comment_id, model.user_id == current_user.id)
    )
    comment = query.scalar_one_or_none()

    if not comment:
        raise HTTPException(404, "Bunday izoh topilmadi.")


async def check_comment_join(db, model, current_user):
    korish = await db.execute(select(model).where(model.user_id == current_user.id))
    result = korish.scalars().all()

    if not result:
        raise HTTPException(404, "Izoh topilmadi")

from fastapi import HTTPException
from datetime import datetime
from sqlalchemy import update

from models.channel import Channel
from sqlalchemy.future import select
from utils.check import check_name
from utils.save_image import save_image


async def create_channel(form, db, current_user):
    await check_name(db, Channel, form)

    channel = await db.execute(
        select(Channel).where(Channel.user_id == current_user.id)
    )
    result = channel.scalar()

    if result:
        raise HTTPException(400, "Siz allaqachon kanal yaratgansiz.")

    new_channel = Channel(
        user_id=current_user.id,
        name=form.name,
        description=form.description,
        created_at=datetime.now(),
    )
    db.add(new_channel)
    await db.commit()


async def create_photo(image, db, current_user):
    channel = await db.execute(
        select(Channel).where(Channel.user_id == current_user.id)
    )
    result = channel.scalar()

    result.profile_image = await save_image(image)
    await db.commit()


async def create_photo_banner(image, db, current_user):
    channel = await db.execute(
        select(Channel).where(Channel.user_id == current_user.id)
    )
    result = channel.scalar()

    result.banner_image = await save_image(image)
    await db.commit()


async def update_channel(form, db, current_user):
    check_name(db, Channel, form)

    await db.execute(
        update(Channel)
        .where(Channel.user_id == current_user.id)
        .values(
            name=form.name,
            description=form.description,
        )
    )
    await db.commit()


async def update_profile_image(image, db, current_user):
    image_path = await save_image(image)

    await db.execute(
        update(Channel)
        .where(Channel.user_id == current_user.id)
        .values(profile_image=image_path)
    )
    await db.commit()


async def update_banner_image(image, db, current_user):
    image_path = await save_image(image)

    await db.execute(
        update(Channel)
        .where(Channel.user_id == current_user.id)
        .values(banner_image=image_path)
    )
    await db.commit()

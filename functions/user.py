from datetime import datetime, timezone
from sqlalchemy import update

from sqlalchemy.future import select
from utils.save_image import save_image
from models.user import User
from utils.check import check_username, check_email
from routers.auth import get_password_hash


async def create_user(form, db):
    await check_username(db, User, form)
    await check_email(db, User, form)

    now = datetime.now(timezone.utc)

    new_user = User(
        username=form.username,
        email=form.email,
        password=get_password_hash(form.password),
        create_at=now,
    )
    db.add(new_user)
    await db.commit()


async def create_photo(image, db, current_user):
    user = await db.execute(select(User).where(User.id == current_user.id))
    result = user.scalar()

    result.image = await save_image(image)
    await db.commit()


async def update_user(form, db, current_user):
    await check_username(db, User, form)
    await check_email(db, User, form)

    await db.execute(
        update(User)
        .where(User.id == current_user.id)
        .values(
            username=form.username,
            email=form.email,
            password=get_password_hash(form.password),
        )
    )
    await db.commit()


async def update_photo(image, db, current_user):
    image_path = await save_image(image)

    await db.execute(
        update(User).where(User.id == current_user.id).values(image=image_path)
    )
    await db.commit()

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, update

from sqlalchemy.future import select
from utils.database import database
from models.subscription import Subscription
from models.channel import Channel
from models.user import User
from schemas.subscription import SchemasSubscription
from schemas.user import SchemasUser
from sqlalchemy.ext.asyncio import AsyncSession
from routers.auth import get_current_active_user
from functions.subscription import create_subscription


subscription_router = APIRouter()


@subscription_router.post("/post_subscription")
async def obuna_bolish(
    form: SchemasSubscription,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    try:
        await create_subscription(form, db, current_user)
        return {"message": "Obuna boldingiz."}

    except Exception as err:
        return {"message": "Xatolik bor!", "Error": str(err)}


@subscription_router.get("/get_subscriptions")
async def obuna_bolgan_kanallarim(
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    try:
        result = await db.execute(
            select(
                Channel.id,
                Channel.name,
                Channel.profile_image,
                Channel.subscription_amount,
                User.username,
                Subscription.created_at,
            )
            .select_from(Subscription)
            .join(Channel, Channel.id == Subscription.channel_id)
            .join(User, User.id == Channel.user_id)
            .where(Subscription.subscriber_id == current_user.id)
        )

        data = result.all()
        if not data:
            raise HTTPException(404, "Siz hech qanday kanalga obuna emassiz.")

        return [
            {
                "id": row.id,
                "channel_name": row.name,
                "channel_profile_image": row.profile_image,
                "channel_subscription_amount": row.subscription_amount,
                "username": row.username,
                "created_at": row.created_at,
            }
            for row in data
        ]

    except Exception as err:
        return {"message": "Xatolik bor!", "Error": str(err)}


@subscription_router.get("/my_subscribers")
async def obuna_bolganlarni_korish(
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    try:
        channel_stmt = select(Channel).where(Channel.user_id == current_user.id)
        channel_result = await db.execute(channel_stmt)
        channel = channel_result.scalar()

        if not channel:
            return {"message": "Sizda hali kanal mavjud emas!"}

        stmt = (
            select(
                Subscription.id,
                User.username,
                User.image,
                Channel.name,
                Subscription.created_at,
            )
            .select_from(Subscription)
            .join(User, User.id == Subscription.subscriber_id)
            .join(Channel, Channel.id == Subscription.channel_id)
            .where(Subscription.channel_id == channel.id)
        )

        result = await db.execute(stmt)
        rows = result.all()

        return [
            {
                "id": row.id,
                "username": row.username,
                "user_image": row.image,
                "channel_name": row.name,
                "created_at": row.created_at,
            }
            for row in rows
        ]

    except Exception as err:
        return {"message": "Xatolik bor!", "Error": str(err)}


@subscription_router.delete("/delete_subscription")
async def obuna_ochirish(
    ident: int,
    db: AsyncSession = Depends(database),
    current_user: SchemasUser = Depends(get_current_active_user),
):
    try:
        result = await db.execute(select(Subscription).where(Subscription.id == ident))
        subscription = result.scalar_one_or_none()

        if not subscription:
            raise HTTPException(404, "Obuna topilmadi.")

        if subscription.subscriber_id != current_user.id:
            raise HTTPException(403, "Ruxsat yo'q.")

        await db.execute(delete(Subscription).where(Subscription.id == ident))

        await db.execute(
            update(Channel)
            .where(Channel.id == subscription.channel_id)
            .values(subscription_amount=Channel.subscription_amount - 1)
        )

        await db.commit()
        return {"message": "Obuna bekor qilindi."}

    except Exception as err:
        return {"message": "Xatolik bor!", "Error": str(err)}

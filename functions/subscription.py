from datetime import datetime, timezone
from sqlalchemy import update

from models.subscription import Subscription
from models.channel import Channel
from utils.check import check_channel, check_have_channel


async def create_subscription(form, db, current_user):
    await check_channel(db, Channel, form)
    await check_have_channel(db, Subscription, form, current_user)

    now = datetime.now(timezone.utc)

    new_subscription = Subscription(
        subscriber_id=current_user.id,
        channel_id=form.channel_id,
        created_at=now,
    )

    db.add(new_subscription)
    await db.execute(
        update(Channel)
        .where(Channel.id == form.channel_id)
        .values(subscription_amount=Channel.subscription_amount + 1)
    )

    await db.commit()

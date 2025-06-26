from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from utils.database import Base


class Subscription(Base):
    __tablename__ = "subscription"

    id = Column(Integer, primary_key=True, autoincrement=True)
    subscriber_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    channel_id = Column(Integer, ForeignKey("channel.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from utils.database import Base


class Channel(Base):
    __tablename__ = "channel"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), unique=True, nullable=False)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    profile_image = Column(String(255), nullable=True)
    banner_image = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    subscription_amount = Column(Integer, default=0, nullable=False)

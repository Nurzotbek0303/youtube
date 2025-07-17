from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from utils.database import Base


class ShortsLike(Base):
    __tablename__ = "shortsLike"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), unique=True, nullable=False)
    video_id = Column(Integer, ForeignKey("shorts.id"), nullable=False)
    is_like = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)

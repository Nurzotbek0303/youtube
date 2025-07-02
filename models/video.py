from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from utils.database import Base


class Video(Base):
    __tablename__ = "video"

    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(Integer, ForeignKey("channel.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    file_path = Column(String(255), nullable=True)
    thumbnail_path = Column(String(255), nullable=True)
    category = Column(String(100), nullable=False)
    views = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    like_amount = Column(Integer, default=0, nullable=False)
    duration_video = Column(Float, nullable=True)
    dislike_amount = Column(Integer, nullable=False, default=0)

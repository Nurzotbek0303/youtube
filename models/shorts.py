from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from utils.database import Base


class Shorts(Base):
    __tablename__ = "shorts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(Integer, ForeignKey("channel.id"), nullable=False)
    video_url = Column(String(255), nullable=True)
    thumbnail_path = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False)

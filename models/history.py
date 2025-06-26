from sqlalchemy import Column, Integer, ForeignKey, DateTime
from utils.database import Base


class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    video_id = Column(Integer, ForeignKey("video.id"), nullable=False)
    watched_at = Column(DateTime(timezone=True), nullable=False)

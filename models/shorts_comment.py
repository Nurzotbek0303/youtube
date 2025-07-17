from sqlalchemy import Column, Integer, DateTime, Text, ForeignKey
from utils.database import Base


class ShortsComment(Base):
    __tablename__ = "shortsComment"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    video_id = Column(Integer, ForeignKey("shorts.id"), nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from utils.database import Base


class Playlist(Base):
    __tablename__ = "playlist"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    is_personal = Column(Boolean, nullable=False)
    channel_id = Column(Integer, ForeignKey("channel.id"), nullable=False)

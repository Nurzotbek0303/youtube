from sqlalchemy import Column, Integer, ForeignKey
from utils.database import Base


class PlaylistVideo(Base):
    __tablename__ = "playlist_video"

    id = Column(Integer, primary_key=True, autoincrement=True)
    playlist_id = Column(Integer, ForeignKey("playlist.id"), nullable=False)
    video_id = Column(Integer, ForeignKey("video.id"), nullable=False)

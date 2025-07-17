from pydantic import BaseModel
from typing import Optional


class SchemasPlaylistVideo(BaseModel):
    playlist_id: int
    video_id: int


class PlaylistVideoResp(BaseModel):
    id: int
    title: str
    file_path: Optional[str] = ""
    is_personal: bool

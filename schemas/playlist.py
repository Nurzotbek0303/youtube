from pydantic import BaseModel, Field
from typing import Optional


class SchemasPlaylist(BaseModel):
    name: str = Field(min_length=3, max_length=200)
    is_personal: bool


class PlaylistResp(BaseModel):
    id: int
    channel_name: str
    playlist_name: str
    is_personal: bool
    image: Optional[str] = ""

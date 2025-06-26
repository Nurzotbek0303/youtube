from pydantic import BaseModel


class SchemasPlaylistVideo(BaseModel):
    playlist_id: int
    video_id: int

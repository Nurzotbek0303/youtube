from pydantic import BaseModel


class SchemasLike(BaseModel):
    video_id: int
    is_like: bool

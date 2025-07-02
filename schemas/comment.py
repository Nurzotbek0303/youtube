from pydantic import BaseModel


class SchemasComment(BaseModel):
    video_id: int
    comment: str

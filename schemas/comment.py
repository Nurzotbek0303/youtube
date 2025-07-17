from pydantic import BaseModel, Field


class SchemasComment(BaseModel):
    video_id: int
    comment: str = Field(min_length=3, max_length=1000)

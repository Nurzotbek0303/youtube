from pydantic import BaseModel


class SchemasSubscription(BaseModel):
    channel_id: int

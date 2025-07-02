from pydantic import BaseModel


class SchemasChannel(BaseModel):
    name: str
    description: str

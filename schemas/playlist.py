from pydantic import BaseModel


class SchemasPlaylist(BaseModel):
    name: str
    is_personal: bool

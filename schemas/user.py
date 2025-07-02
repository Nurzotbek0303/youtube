from pydantic import BaseModel, EmailStr


class SchemasUser(BaseModel):
    username: str
    email: EmailStr
    password: str

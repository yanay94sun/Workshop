from pydantic import BaseModel


class UserID(BaseModel):
    id: str

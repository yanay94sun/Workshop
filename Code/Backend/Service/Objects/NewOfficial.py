from pydantic import BaseModel


class newOfficial(BaseModel):
    user_id: str
    store_id: str
    new_owner_name: str

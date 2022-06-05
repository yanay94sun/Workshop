from pydantic import BaseModel


class Store_name(BaseModel):
    store_name: str
    id: str

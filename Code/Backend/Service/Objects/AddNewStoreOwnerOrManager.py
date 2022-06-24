from pydantic import BaseModel
from pydantic.class_validators import Optional


class AddNewStoreOwnerOrManager(BaseModel):
    store_id: str
    to_add_id: str

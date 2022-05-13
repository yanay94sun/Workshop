from pydantic import BaseModel
from typing import Optional


class TokenData(BaseModel):
    # TODO temporary, gonna be fixed
    id: Optional[str] = None

from pydantic import BaseModel
from pydantic.class_validators import Optional


class Dog(BaseModel):
    name: str
    owner: str


class Dogy():
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner


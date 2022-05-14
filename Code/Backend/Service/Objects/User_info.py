from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from pydantic.class_validators import Optional
from random import randrange


class User_info(BaseModel):
    username: str
    password: str

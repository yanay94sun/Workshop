from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from pydantic.class_validators import Optional
from random import randrange

from Code.Backend.Service.Service import Service

app = FastAPI()

# for prod end RUN IN COMMEND LINE: uvicorn Server:app
# for dev env RUN IN COMMEND LINE: uvicorn Server:app --reload


service = Service()

# contract with frontEnd, what we expect to get from the post request


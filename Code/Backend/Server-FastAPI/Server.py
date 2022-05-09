from fastapi import FastAPI, Response, status, HTTPException, Depends, Cookie
from fastapi.params import Body
from pydantic import BaseModel
from pydantic.class_validators import Optional
from random import randrange
from fastapi.middleware.cors import CORSMiddleware
# from Code.Backend.FastAPI import utils

from jose import JWTError, jwt
from datetime import datetime, timedelta

# print(os.getcwd())
from passlib.context import CryptContext

# hashing passwords


from Code.Backend.Service.Objects.PaymentService import PaymentService
from Code.Backend.Service.Objects.SupplySevice import SupplyService
from Code.Backend.Service.Objects.TokenData import TokenData
from Code.Backend.Service.Objects.User_info import User_info
from Code.Backend.Service.Service import Service

# from Code.Backend.FastAPI import utils

service = Service()
service.initial_system(payment_service=PaymentService(), supply_service=SupplyService())

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# RUN IN COMMEND LINE FROM WorkshopProj dir terminal: uvicorn Code.Backend.Server-FastAPI.Server:app --reload

# contract with frontEnd, what we expect to get from the post request

# aaa
# YA TAMBALLLL
# ya zain
# lech tizdayen

"""
main page aka root
"""


@app.get("/")
def root():
    return {"message": "Welcome to our site!"}


"""
---------------------------------------------------
Users requirements
General guest actions
---------------------------------------------------
"""


@app.get("/guests/enter")
def enter_as_guest(response: Response):
    res = service.enter_as_guest()
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something's wrong with the server, cant reach site")
    response.set_cookie(key="user_id", value=res.value)
    return res


@app.post("/guests/login")
def login(user_info: User_info, user_id: Optional[str] = Cookie(None)):
    print(user_id)
    # hashed_password = hash_pass(user_info.password)
    res = service.login(user_id, user_info.username, user_info.password)
    if res.error_occurred():
        # TODO to change detail msg to non informative one for security reasons
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res.msg)

    # create a token
    # return token

    access_token = create_access_token(data={"user_id": user_id})

    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/guests/register")
def register(user_info: User_info, user_id: Optional[str] = Cookie(None)):
    # hash the password - user.password
    hash_password = hash_pass(user_info.password)
    user_info.password = hash_password
    user_info_dict = user_info.dict()
    res = service.register(user_id, user_info_dict)
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res.msg)
    return {"data": user_info_dict}


@app.post("/users/get_store_info")
def get_store_info(store_id: str):
    res = service.get_store_info(store_id)
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res.msg)
    return res.value


"""
--------------------------------------
Member's purchase actions
--------------------------------------
"""


@app.post("/users/logout")
def logout(user_id: Optional[str] = Cookie(None)):
    res = service.logout(user_id)
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res.msg)
    return Response(status_code=status.HTTP_200_OK)


@app.post("users/open_store")
def open_store(user_id: str, store_name: str):
    res = service.open_store(user_id, store_name)
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=res.msg)
    return res


"""
------------------------------------------------------------------------
                                    Utils
------------------------------------------------------------------------
"""


def hash_pass(password: str):
    return pwd_context.hash(password)


"""
------------------------------------------------------------------------
                                    TODO
                NEED TO MOVE TO DIFFERENT FILE, IMPORTS PROBLEMS!
------------------------------------------------------------------------
"""

# SECRET_KEY
# Algorithm
# Expiration time

SECRET_KEY = "09d25e049faa6ca2556a818196b7a3563b91f7099f6f0f4caa6cf63b88e2d9e6"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    __to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    __to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(__to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, user_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        user_id: str = payload.get("user_id")

        if user_id is None:
            raise user_exception
        token_data = TokenData(id=user_id)

    except JWTError:
        raise user_exception

    return token_data

# def get_current_user(token: str = Depends())

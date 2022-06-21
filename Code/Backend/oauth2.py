# from fastapi import FastAPI, Response, status, HTTPException, Depends, Cookie
# from fastapi.params import Body
# from pydantic import BaseModel
# from pydantic.class_validators import Optional
# from random import randrange
# from fastapi.middleware.cors import CORSMiddleware
# # from Code.Backend.FastAPI import utils
# from fastapi.security.oauth2 import OAuth2PasswordRequestForm
# from jose import JWTError, jwt
# from datetime import datetime, timedelta
# from fastapi.security import OAuth2PasswordBearer
#
# # print(os.getcwd())
# from passlib.context import CryptContext
#
# from Code.Backend.Service.Objects.PaymentService import PaymentService
# from Code.Backend.Service.Objects.SupplySevice import SupplyService
# from Code.Backend.Service.Objects.TokenData import TokenData
# from Code.Backend.Service.Objects.User_info import User_info
# from Code.Backend.Service.Service import Service
#
# # from Code.Backend.FastAPI import utils
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="guests/login")
#
# # SECRET_KEY
# # Algorithm
# # Expiration time
#
# SECRET_KEY = "09d25e049faa6ca2556a818196b7a3563b91f7099f6f0f4caa6cf63b88e2d9e6"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
#
#
# def create_access_token(data: dict):
#     __to_encode = data.copy()
#
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     __to_encode.update({"exp": expire})
#
#     encoded_jwt = jwt.encode(__to_encode, SECRET_KEY, algorithm=ALGORITHM)
#
#     return encoded_jwt
#
#
# def verify_access_token(token: str, user_exception):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
#
#         user_id: str = payload.get("user_id")
#
#         if user_id is None:
#             raise user_exception
#         token_data = TokenData(id=user_id)
#
#     except JWTError:
#         raise user_exception
#
#     return token_data
#
#
# def get_current_user(token: str = Depends(oauth2_scheme)):
#     user_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                                    detail="could not validate user", headers={"WWW-Authenticate": "Bearer"})
#     return verify_access_token(token, user_exception)
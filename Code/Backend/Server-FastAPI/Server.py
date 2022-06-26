import sys
from random import random
from typing import List

from fastapi import FastAPI, Response, status, HTTPException, WebSocket, Depends, Cookie
from fastapi.params import Body
from pydantic import BaseModel
from pydantic.class_validators import Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi_socketio import SocketManager

# from Code.Backend.FastAPI import utils
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from starlette.websockets import WebSocketDisconnect

from Code.Backend.Domain.DomainDataObjects.ProductPurchaseRequest import ProductPurchaseRequest
from Code.Backend.Service.Objects.Discount import Discount
from Code.Backend.Service.Objects.DiscountCompose import DiscountCompose
from Code.Backend.Service.Objects.EditProduct import EditProduct
from Code.Backend.Service.Objects.NewOfficial import newOfficial
from Code.Backend.Service.Objects.AddProduct import AddProduct
from Code.Backend.Service.Objects.NewProudct import NewProduct
from Code.Backend.Service.Objects.PackageInfo import PackageInfo
from Code.Backend.Service.Objects.PaymentInfo import PaymentInfo
from Code.Backend.Service.Objects.PaymentService import PaymentService
from Code.Backend.Service.Objects.ProductInfo import ProductInfo
from Code.Backend.Service.Objects.ProductSearchFilters import ProductSearchFilters
from Code.Backend.Service.Objects.StoreName import Store_name
from Code.Backend.Service.Objects.SupplySevice import SupplyService
from Code.Backend.Service.Objects.TokenData import TokenData
from Code.Backend.Service.Objects.UserID import UserID
from Code.Backend.Service.Objects.User_info import User_info
from Code.Backend.Service.Service import Service

# from Code.Backend import oauth2


"""
                                     IMPORTANT!!!
-----------------------------------------------------------------------------------------------------------------
- please make sure that your current dirctory is WorkshopProj/

- for install all packages needed please run in terminal: pip install -r requirements.txt

- to run the server run in terminal: uvicorn Code.Backend.Server-FastAPI.Server:app --reload
                        
                        
                        thank you,
                        legolas94sun
"""

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="guests/login")
try:
    service = Service()
    service.initial_system(payment_service=PaymentService(), supply_service=SupplyService(), path='config.ini')
except ValueError as e:
    sys.exit(e.args)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # CORSMiddleware,
    # allow_origins=origins,
    # allow_credentials=True,
    # allow_methods=[
    #     "GET",
    #     "POST",
    #     "OPTIONS",
    # ],  # include additional methods as per the application demand
    # allow_headers=[
    #     "Content-Type",
    #     "Set-Cookie",
    # ],  # include additional headers as per the application demand
)

"""
WebSocket - SocketIO
"""
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        try:

            await websocket.send_text(message)
        except WebSocketDisconnect:
            manager.disconnect(websocket)
            # await manager.broadcast(f"Client #{client_id} left the chat")
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print('A new websocket to create.')
    # await websocket.accept()
    await manager.connect(websocket)
    print("Accepted")
    try:
        while True:
            # Wait for any message from the client
            data = await websocket.receive_text()
            websocket.join(data)
            print(data)
            # res  = service.getuser
            # Send message to the client
            resp = {'value': random.uniform(0, 1)}
            await websocket.send_json(resp)
    # except Exception as e:
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # await manager.broadcast(f"Client #{client_id} left the chat")
        print('error:', e)
            # break
    print('Bye..')


# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     print('A new websocket to create.')
#     await websocket.accept()
#     print("Accepted")
#     while True:
#         try:
#             # Wait for any message from the client
#             data = await websocket.receive_text()
#             websocket.join(data)
#             print(data)
#             # res  = service.getuser
#             # Send message to the client
#             resp = {'value': random.uniform(0, 1)}
#             await websocket.send_json(resp)
#         except Exception as e:
#             print('error:', e)
#             break
#     print('Bye..')
#
# def update(user_id):
#     ## conncetion
#     ws.send.to(user_id)


# @socket_manager.on('client_start_event')
# async def handle_client_start_event(sid, *args, **kwargs): # (!)
#     print('Server says: start_event worked')
#     await socket_manager.emit('server_antwort01',{'data':'start event worked'})


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


#


@app.get("/guests/enter")
def enter_as_guest(response: Response):
    res = service.enter_as_guest()
    if res.error_occurred():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something's wrong with the server, cant reach site",
        )
    response.set_cookie(
        key="user_id", value=res.value, httponly=True, samesite="None", secure=True
        # key="user_id", value=res.value
    )
    return res


@app.post("/exit")
def exit_site(user_id: UserID):  # Optional[str] = Cookie(None)):
    res = service.exit(user_id.id)
    if res.error_occurred():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something's wrong with the server"
        )
    return res


@app.post("/guests/login")
def login(
        user_info: User_info):  # ,        user_id: Optional[str] = Cookie(None),):
    hashed_password = hash_pass(user_info.password)
    res = service.login(user_info.id, user_info.username, user_info.password)  # user_info.password)
    print(user_info.id)
    print("PASS: " + hashed_password)
    if res.error_occurred():
        # TODO to change detail msg to non informative one for security reasons
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="wrong details")

    # create a token
    # return token

    # access_token = oauth2.create_access_token(data={"user_id": user_info.id})

    return {"response": res, "token_type": "bearer"}


@app.post("/guests/register")
def register(user_info: User_info):  # , user_id: Optional[str] = Cookie(None)):
    # hash the password - user.password
    print(user_info)
    # hash_password = hash_pass(user_info.password)
    # user_info.password = hash_password
    user_info_dict = user_info.dict()
    res = service.register(user_info.id, user_info_dict)
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res.msg)
    return {"data": res.value}


@app.get("/stores/{store_id}")
def get_store_info(store_id: str):
    res = service.get_store_info(store_id)
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res.msg)
    return res.value


@app.get("/get_cart_price/{user_id}")
def get_cart_price(user_id: str):
    res = service.get_cart_price(user_id)
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res.msg)
    return res.value


@app.get("/stores")
def get_stores_info():
    res = service.get_stores_info()
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res.msg)
    return res.value


@app.post("/add_product_to_shopping_cart")
def add_product_to_shopping_cart(add_product: AddProduct):  # , user_id: Optional[str] = Cookie(None)):
    print(add_product)
    res = service.add_product_to_shopping_cart(
        add_product.id, add_product.store_id, add_product.product_id, add_product.quantity
    )
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=res.msg)
    return res.value


@app.get("/cart/{user_id}")
def get_shopping_cart(user_id: str):  #: Optional[str] = Cookie(None)):
    res = service.get_shopping_cart(user_id)
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res.msg)
    return res.value


@app.post("/products/search")
def search_product(product_search_filters: ProductSearchFilters):
    res = service.search_product(product_search_filters)
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res.msg)
    return res.value


@app.get("/product/{store_id}/{product_id}")
def get_product_and_his_quantities(store_id: str, product_id: str):
    res = service.get_product_and_quantities(store_id, product_id)
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res.msg)
    return res.value


@app.get("/users/{user_id}")
def get_users_stores(user_id: str):
    res = service.get_users_stores(user_id)
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res.msg)
    return res.value


# @TODO no ProductPurchaseRequest service object, need to do
# @app.delete("/cart/remove_product", status_code=status.HTTP_204_NO_CONTENT)
# def remove_product_from_shopping_cart(ppr: ProductPurchaseRequest, user_id: Optional[str] = Cookie(None)):
#     res = service.remove_product_from_shopping_cart(user_id, ppr)
#     if res.error_occurred():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res.msg)
#     return res.value


@app.post("/pay")
def purchase_shopping_cart(payment_info: PaymentInfo):
    res = service.purchase_shopping_cart(payment_info.customer_id, payment_info)
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res.msg)
    return res.value


@app.post("/supply")
def contact_supply_service(package_info: PackageInfo):
    res = service.contact_supply_service(package_info)
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res.msg)
    return res.value


@app.post("/discount/visible/product")
def add_visible_discount_by_product(discount: Discount):
    res = service.add_visible_discount_by_product(discount.user_id, discount.store_id, discount.discount_price,
                                                  discount.end_date, discount.product_id)
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=res.msg)
    return res.value


@app.post("/discount/visible/category")
def add_visible_discount_by_category(discount: Discount):
    res = service.add_visible_discount_by_category(discount.user_id, discount.store_id, discount.discount_price,
                                                   discount.end_date, discount.category_name)
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=res.msg)
    return res.value


@app.post("/discount/visible/store")
def add_visible_discount_by_store(discount: Discount):
    res = service.add_visible_discount_by_store(discount.user_id, discount.store_id, discount.discount_price,
                                                discount.end_date)
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=res.msg)
    return res.value


@app.post("/discount/conditional/product")
def add_conditional_discount_by_product(discount: Discount):
    res = service.add_conditional_discount_by_product(discount.user_id, discount.store_id, discount.discount_price,
                                                      discount.end_date,
                                                      discount.product_id,
                                                      discount.dic_of_products_and_quantity,
                                                      discount.min_price_for_discount)
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=res.msg)
    return res.value


@app.post("/discount/conditional/category")
def add_conditional_discount_by_category(discount: Discount):
    res = service.add_conditional_discount_by_category(discount.user_id, discount.store_id, discount.discount_price,
                                                       discount.end_date,
                                                       discount.category_name,
                                                       discount.dic_of_products_and_quantity,
                                                       discount.min_price_for_discount)
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=res.msg)
    return res.value


@app.post("/discount/conditional/store")
def add_conditional_discount_by_store(discount: Discount):
    res = service.add_conditional_discount_by_store(discount.user_id, discount.store_id, discount.discount_price,
                                                    discount.end_date,
                                                    discount.dic_of_products_and_quantity,
                                                    discount.min_price_for_discount)
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=res.msg)
    return res.value


@app.post("/discount/or")
def add_or_discount(discount: DiscountCompose):
    res = service.add_or_discount(discount.user_id,
                                  discount.store_id, discount.first_discount_id,
                                  discount.second_discount_id)
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=res.msg)
    return res.value


@app.post("/discount/and")
def add_and_discount(discount: DiscountCompose):
    res = service.add_and_discount(discount.user_id,
                                   discount.store_id, discount.first_discount_id,
                                   discount.second_discount_id)
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=res.msg)
    return res.value


@app.post("/discount/xor")
def add_xor_discount(discount: DiscountCompose):
    res = service.add_xor_discount(discount.user_id,
                                   discount.store_id, discount.first_discount_id,
                                   discount.second_discount_id)
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=res.msg)
    return res.value


@app.post("/discount/sum")
def add_sum_discount(discount: DiscountCompose):
    res = service.add_sum_discount(discount.user_id,
                                   discount.store_id, discount.first_discount_id,
                                   discount.second_discount_id)
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=res.msg)
    return res.value


@app.post("/discount/max")
def add_max_discount(discount: DiscountCompose):
    res = service.add_max_discount(discount.user_id,
                                   discount.store_id, discount.first_discount_id,
                                   discount.second_discount_id)
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=res.msg)
    return res.value


"""
--------------------------------------
Member's purchase actions
--------------------------------------
"""


@app.post("/users/logout")
def logout(user_id: UserID):  #: Optional[str] = Cookie(None)):
    res = service.logout(user_id.id)
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res.msg)
    return Response(status_code=status.HTTP_200_OK)


@app.post("/users/open_store")
def open_store(store_name: Store_name):  # , user_id: Optional[str] = Cookie(None)):
    res = service.open_store(store_name.id, store_name.store_name)
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=res.msg)
    return res.value


@app.post("/users/add_new_product_to_inventory")
def add_new_product_to_inventory(
        new_product: NewProduct):  # , user_id: Optional[str] = Cookie(None)):
    res = service.add_new_product_to_inventory(
        new_product.id, new_product.store_id, new_product.name, new_product.description, new_product.price,
        new_product.category
    )
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=res.msg)
    return res.value


@app.post("/users/add_products_to_inventory")
def add_products_to_inventory(
        add_product: AddProduct):  # , user_id: Optional[str] = Cookie(None)):
    res = service.add_products_to_inventory(
        add_product.id, add_product.store_id, add_product.product_id, add_product.quantity
    )
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=res.msg)
    return res.value


@app.get("/permission/{store_id}/{user_id}")
def get_permissions(store_id: str, user_id: str):
    res = service.get_permissions(store_id, user_id)
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res.msg)
    return res.value


# @TODO not working
@app.post("/users/remove_products_from_inventory")
def remove_products_from_inventory(add_product: AddProduct):
    res = service.remove_products_from_inventory(
        add_product.id, add_product.store_id, add_product.product_id, add_product.quantity
    )
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res.msg)
    return res.value


@app.post("/users/edit_product_info")
def edit_product_info(edit_product: EditProduct):
    info = ProductInfo(name=edit_product.name, description=edit_product.description,
                       rating=edit_product.rating, price=edit_product.price, category=edit_product.category)
    res = service.edit_product_info(edit_product.id, edit_product.store_id, edit_product.product_id, info)
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=res.msg)
    return res.value


@app.post("/users/add_store_owner")
def add_store_owner(official: newOfficial):
    res = service.add_store_owner(official.user_id, official.store_id, official.new_owner_name)
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=res.msg)
    return res.value


@app.post("/users/add_store_manager")
def add_store_manager(official: newOfficial):
    res = service.add_store_manager(official.user_id, official.store_id, official.new_owner_name)
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=res.msg)
    return res.value


@app.post("/users/get_store_roles")
def get_store_roles(store: Store_name):
    res = service.get_store_roles(store.id, store.store_name)
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=res.msg)
    return res.value


@app.get("/check_connection/{user_id}")
def check_connection(user_id: str):
    res = service.check_connection(user_id)
    if res.error_occurred():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res.msg)
    return res.value


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

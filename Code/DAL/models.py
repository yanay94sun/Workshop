from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql.expression import null, text
from Code.DAL.database import Base


class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, nullable=False)
    password = Column(String, nullable=False)


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, ForeignKey("users.username", onupdate="CASCADE"), nullable=False)
    message = Column(String, nullable=False)


class Store(Base):
    __tablename__ = "stores"

    store_id = Column(Integer, primary_key=True, nullable=False)
    is_active = Column(Boolean, server_default='TRUE', nullable=False)
    purchase_policy = Column(Integer, nullable=False)
    display_policy = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    founder = Column(String, ForeignKey("users.username", onupdate="CASCADE"), nullable=False)
    id_counter = Column(Integer, nullable=False)


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    store_id = Column(Integer, ForeignKey("stores.store_id", onupdate="CASCADE"), nullable=False)


class ShoppingBasket(Base):
    __tablename__ = "shoppingBaskets"

    id = Column(Integer, primary_key=True, nullable=False)
    store_id = Column(Integer, ForeignKey("stores.store_id", onupdate="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.product_id", onupdate="CASCADE"), nullable=False)
    username = Column(String, ForeignKey("users.username"), nullable=False)
    quantity = Column(Integer, nullable=False)


class Official(Base):
    __tablename__ = "officials"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, ForeignKey("users.username", onupdate="CASCADE"), nullable=False)
    appointee = Column(String, ForeignKey("users.username", onupdate="CASCADE"), nullable=False)
    store_id = Column(Integer, ForeignKey("stores.store_id", onupdate="CASCADE"), nullable=False)
    INVENTORY_ACTION = Column(Boolean, server_default="FALSE", nullable=False)
    CHANGE_MANAGER_PERMISSION = Column(Boolean, server_default="FALSE", nullable=False)
    ADD_STORE_MANAGER = Column(Boolean, server_default="FALSE", nullable=False)
    ADD_STORE_OWNER = Column(Boolean, server_default="FALSE", nullable=False)
    GET_STORE_PURCHASE_HISTORY = Column(Boolean, server_default="FALSE", nullable=False)
    CLOSE_STORE = Column(Boolean, server_default="FALSE", nullable=False)
    GET_STORE_ROLES = Column(Boolean, server_default="FALSE", nullable=False)
    PURCHASE_MANAGEMENT = Column(Boolean, server_default="FALSE", nullable=False)
    DISCOUNT_MANAGEMENT = Column(Boolean, server_default="FALSE", nullable=False)
    is_owner = Column(Boolean, server_default="FALSE", nullable=False)




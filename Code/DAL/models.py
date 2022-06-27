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
    name = Column(String, nullable=False)
    is_active = Column(Boolean, server_default='TRUE', nullable=False)
    # purchase_policy = Column(Integer, nullable=False)
    # discount_policy = Column(Integer, nullable=False)
    founder_username = Column(String, ForeignKey("users.username", onupdate="CASCADE"), nullable=False)
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


class ShoppingBasketItem(Base):
    __tablename__ = "shoppingBasketItems"

    store_id = Column(Integer, ForeignKey("stores.store_id", onupdate="CASCADE"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.product_id", onupdate="CASCADE"), nullable=False,
                        primary_key=True)
    username = Column(String, ForeignKey("users.username"), nullable=False)
    quantity = Column(Integer, nullable=False)


class Official(Base):
    __tablename__ = "officials"

    # id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, ForeignKey("users.username", onupdate="CASCADE"), primary_key=True, nullable=False)
    appointee = Column(String, ForeignKey("users.username", onupdate="CASCADE"), nullable=False)
    store_id = Column(Integer, ForeignKey("stores.store_id", onupdate="CASCADE"), primary_key=True, nullable=False)
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


class DiscountPolicy(Base):
    __tablename__ = "discount_policies"

    policy_id = Column(Integer, primary_key=True, nullable=False)
    store_id = Column(Integer, ForeignKey("stores.store_id", onupdate="CASCADE"), nullable=False)
    id_counter = Column(Integer)


class Discount(Base):
    __tablename__ = "discounts"

    id = Column(Integer, primary_key=True, nullable=False)
    discount_on = Column(Boolean, server_default="FALSE", nullable=False)
    end_date = Column(TIMESTAMP(timezone=True), nullable=False)
    type = Column(Integer)
    discount_policy_id = Column(Integer, ForeignKey("discount_policies.policy_id", onupdate="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id", onupdate="CASCADE"))
    min_count_of_product = Column(Integer)
    min_price_of_product = Column(Integer)
    is_visible = Column(Boolean)


class ComplexDiscount(Base):
    __tablename__ = "complex_discounts"

    id = Column(Integer, primary_key=True, nullable=False)
    first_discount_id = Column(Integer, ForeignKey("discounts.id", onupdate="CASCADE"), nullable=False)
    second_discount_id = Column(Integer, ForeignKey("discounts.id", onupdate="CASCADE"), nullable=False)
    type = Column(Integer)  # and/or/cond...
    discount_policy_id = Column(Integer, ForeignKey("discount_policies.policy_id", onupdate="CASCADE"), nullable=False)


class PurchasePolicy(Base):
    __tablename__ = "purchase_policies"

    policy_id = Column(Integer, primary_key=True, nullable=False)
    store_id = Column(Integer, ForeignKey("stores.store_id", onupdate="CASCADE"), nullable=False)
    id_counter = Column(Integer)


class PurchaseRule(Base):
    __tablename__ = "purchase_rules"

    id = Column(Integer, primary_key=True, nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id", onupdate="CASCADE"))
    quantity = Column(Integer)
    min_price_to_have = Column(Integer)
    category = Column(String)
    purchase_policy_id = Column(Integer, ForeignKey("purchase_policies.policy_id", onupdate="CASCADE"), nullable=False)


class ComplexPurchaseRule(Base):
    __tablename__ = "complex_purchase_rules"

    id = Column(Integer, primary_key=True, nullable=False)
    first_rule_id = Column(Integer, ForeignKey("purchase_rules.id", onupdate="CASCADE"), nullable=False)
    second_rule_id = Column(Integer, ForeignKey("purchase_rules.id", onupdate="CASCADE"), nullable=False)
    type = Column(Integer)  # and/or/cond...
    purchase_policy_id = Column(Integer, ForeignKey("purchase_policies.policy_id", onupdate="CASCADE"), nullable=False)

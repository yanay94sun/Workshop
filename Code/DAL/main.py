from typing import List

from sqlalchemy.orm import Session

from Code.DAL import models
from Code.DAL.Objects.store import StoreBase, PurchasePolicy, DiscountPolicy, Product, Official, Store
from Code.DAL.Objects.user import User, Notification, ShoppingBasket, UserBase
from Code.DAL.database import engine, get_db

models.Base.metadata.create_all(bind=engine)


def get_user(username: str, db: Session = next(get_db())):
    """
    :param db:
    :param username:
    :return: User object if exists, else None
    """
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        print(f"user \"{username}\" not found")
        return user
    notifications = db.query(models.Notification).filter(models.Notification.username == username).all()
    shopping_baskets = db.query(models.ShoppingBasket).filter(models.ShoppingBasket.username == username).all()

    return User(
        user=UserBase.from_orm(user),
        shopping_cart=(ShoppingBasket.from_orm(s) for s in shopping_baskets),
        notifications=(Notification.from_orm(n) for n in notifications)
    )


def persist_user(user: UserBase,
                 notifications: List[str] = (),
                 shopping_cart: List[ShoppingBasket] = (),
                 db: Session = next(get_db())) -> User:
    """
    :param db:
    :param user: a UserBase like includes username, password
    :param notifications: a list of messages
    :param shopping_cart: a list of ShoppingBasket object
    :return: an updated orm if successful, None otherwise.
    """
    new_user = models.User(**user.dict())  # creating a user orm
    new_notifications = [models.Notification(username=user.username, message=n) for n in notifications]
    new_baskets = [models.ShoppingBasket(**basket.dict(), username=user.username) for basket in shopping_cart]
    for instance in new_notifications + new_baskets:
        db.add(instance)
    db.add(new_user)
    db.commit()
    for instance in new_notifications + new_baskets:
        db.refresh(instance)
    db.refresh(new_user)
    return User(user=new_user, shopping_cart=new_baskets, notifications=new_notifications)


def delete_user(username: str) -> bool:
    """
    delete a user
    :param username: the user's username
    :return: True if successful, False otherwise
    """


def persist_store(store: StoreBase,
                  purchase_policy: PurchasePolicy,
                  discount_policy: DiscountPolicy,
                  products: List[Product],
                  officials: List[Official],
                  db: Session = get_db()
                  ):
    """
    :param db:
    :param store: basic fields -> store_id: str, is_active: bool, name: str, founder_username: str, id_counter: int
    :param purchase_policy: see in objects
    :param discount_policy: see in objects
    :param products: see in objects
    :param officials: see in objects
    :return: an updated orm if successful, None otherwise.
    """


def get_store(store_id: int, db: Session = get_db()) -> Store:
    """
    :param db:
    :param store_id:
    :return: Store object if exists, None otherwise.
    """


def delete_store(store_id: int) -> bool:
    """
    delete a store and all products and baskets related
    :param store_id: store's id
    :return: True if successful, False otherwise
    """


def persist_product(store_id: int, product: Product) -> Product:
    """
    persisting a new product when adding to store's inventory.
    :param store_id: store's id
    :param product: see in Objects
    :return: an updated orm if successful, None otherwise.
    """


def delete_product(product_id: int) -> bool:
    """
    delete a product and all related shipping baskets
    :param product_id:
    :return: True if successful, False otherwise.
    """


def persist_official(store_id: int, official: Official) -> Official:
    """
    persisting a new official to store
    :param store_id: store's id
    :param official: see in Objects
    :return: an updated orm if successful, None otherwise.
    """


def delete_official(store_id: int, official_username: str) -> bool:
    """
    delete an official from store
    :param store_id: store's id
    :param official_username: the official username
    :return: True if successful, False otherwise.
    """


def persist_shopping_basket(username: str, basket: ShoppingBasket) -> ShoppingBasket:
    """
    persisting a new shopping basket (collecting all baskets into a cart when requested)
    :param username: the username related to the basket
    :param basket: see in Objects
    :return: an updated orm if successful, None otherwise.
    """


def delete_shopping_basket(username: str, store_id: int) -> bool:
    """
    delete a shopping basket
    :param username: the user's basket
    :param store_id: the related store to the basket
    :return: True if successful, False otherwise.
    """

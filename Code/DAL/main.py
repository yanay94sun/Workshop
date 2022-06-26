from typing import List

from sqlalchemy.orm import Session

from Code.DAL import models
from Code.DAL.Objects.store import StoreBase, PurchasePolicy, DiscountPolicy, Product, Official
from Code.DAL.Objects.user import User, Notification, ShoppingBasket, UserBase
from Code.DAL.database import engine, get_db

models.Base.metadata.create_all(bind=engine)


def get_user(username: str, db: Session = get_db()):
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

    user_out = {
        "user": UserBase.from_orm(user),
        "shopping_cart": (ShoppingBasket.from_orm(s) for s in shopping_baskets),
        "notifications": (Notification.from_orm(n) for n in notifications)
    }
    return User(**user_out)


def persist_user(user: UserBase, notifications: List[str], shopping_cart: List[ShoppingBasket], db: Session = get_db()):
    """
    :param db:
    :param user: a UserBase like includes username, password
    :param notifications: a list of messages
    :param shopping_cart: a list of ShoppingBasket object
    :return: an updated orm if successful, None otherwise.
    """
    new_user = models.User(**user.dict())
    new_notification = [models.Notification(username=user.username, message=n) for n in notifications]
    ner = []
    for n in notifications:
        noti = models.Notification(username=user.username, message=n)
        ner.append(noti)
        db.add(noti)

    new_baskets = [models.ShoppingBasket(**basket.dict(), username=user.username) for basket in shopping_cart]
    db.add(new_user)


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


def get_store(store_id: int, db: Session = get_db()):
    """
    :param db:
    :param store_id:
    :return: Store object if exists, None otherwise.
    """

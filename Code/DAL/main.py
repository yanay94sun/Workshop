from typing import List, Tuple, Callable

from sqlalchemy.orm import Session

from Code.DAL import models
from Code.DAL.Objects.store import StoreBase, PurchasePolicy, DiscountPolicy, Product, Official, Store
from Code.DAL.Objects.user import User, Notification, ShoppingBasketItem, UserBase
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
    shopping_baskets = db.query(models.ShoppingBasketItem).filter(models.ShoppingBasketItem.username == username).all()

    return User(
        user=UserBase.from_orm(user),
        shopping_cart=(ShoppingBasketItem.from_orm(s) for s in shopping_baskets),
        notifications=(Notification.from_orm(n) for n in notifications)
    )


def persist_user(user: UserBase,
                 notifications: List[str] = None,
                 shopping_cart: List[ShoppingBasketItem] = None,
                 db: Session = next(get_db())) -> User:
    """
    :param db:
    :param user: a UserBase like includes username, password
    :param notifications: a list of messages
    :param shopping_cart: a list of ShoppingBasket object
    :return: an updated orm if successful, None otherwise.
    """
    if not notifications:
        notifications = []
    if not shopping_cart:
        shopping_cart = []
    new_user = models.User(**user.dict())  # creating a user orm
    new_notifications = [models.Notification(username=user.username, message=n) for n in notifications]
    new_baskets = [models.ShoppingBasketItem(**basket.dict(), username=user.username) for basket in shopping_cart]
    for instance in new_notifications + new_baskets:
        db.add(instance)
    db.add(new_user)
    db.commit()
    for instance in new_notifications + new_baskets:
        db.refresh(instance)
    db.refresh(new_user)
    return User(user=new_user, shopping_cart=new_baskets, notifications=new_notifications)


def delete_user(username: str, db: Session = next(get_db())) -> bool:
    """
    delete a user
    :param db:
    :param username: the user's username
    :return: True if successful, False otherwise
    """
    user = db.query(models.User).filter(models.User.username == username)
    if not user.first():
        return False
    user.delete(synchronize_session=False)
    db.commit()
    return True


def persist_store(store: StoreBase,
                  products: List[Product] = None,
                  officials: List[Official] = None,
                  purchase_policy: PurchasePolicy = None,
                  discount_policy: DiscountPolicy = None,
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
    if not products:
        products = []
    if not officials:
        officials = []
    new_store = models.Store(**store.dict())
    new_products = [models.Product(**p.dict(), store_id=store.store_id) for p in products]
    new_officials = [models.Official(**official.dict(), store_id=store.store_id) for official in officials]
    # TODO: implement
    new_purchase_policy = None
    new_discount_policy = None
    for instance in new_officials + new_products:
        db.add(instance)
    db.add(new_store)
    db.commit()
    for instance in new_officials + new_products:
        db.refresh(instance)
    db.refresh(new_store)
    return Store(store=new_store,
                 purchase_policy=new_purchase_policy,
                 discount_policy=new_discount_policy,
                 products=new_products,
                 officials=new_officials)


def get_store(store_id: int, db: Session = get_db()) -> Store:
    """
    :param db:
    :param store_id:
    :return: Store object if exists, None otherwise.
    """
    store = db.query(models.Store).filter(models.Store.store_id == store_id).first()
    if not store:
        return store
    purchase_policy = None
    discount_policy = None
    products = db.query(models.Product).filter(models.Product.store_id == store_id).all()
    officials = db.query(models.Official).filter(models.Official.store_id == store_id).all()
    return Store(
        store=StoreBase.from_orm(store),
        purchase_policy=None,
        discount_policy=None,
        products=(Product.from_orm(p) for p in products),
        officials=(Official.from_orm(official) for official in officials)
    )


def delete_store(store_id: int, db: Session = next(get_db())) -> bool:
    """
    delete a store and all products and baskets related
    :param db:
    :param store_id: store's id
    :return: True if successful, False otherwise
    """
    return delete_(models.Store, models.Store.store_id == store_id, db=db)
    # store = db.query(models.Store).filter(models.Store.store_id == store_id)
    # if not store.first():
    #     return False
    # store.delete(synchronize_session=False)
    # db.commit()
    # return True


def persist_product(store_id: int, product: Product, db: Session = next(get_db())) -> Product:
    """
    persisting a new product when adding to store's inventory.
    :param db:
    :param store_id: store's id
    :param product: see in Objects
    :return: an updated orm if successful, None otherwise.
    """
    new_product = models.Product(**product.dict(), store_id=store_id)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def delete_product(product_id: int, db: Session = next(get_db())) -> bool:
    """
    delete a product and all related shipping baskets
    :param db:
    :param product_id:
    :return: True if successful, False otherwise.
    """
    return delete_(models.Product, models.Product.product_id == product_id, db=db)
    # product = db.query(models.Product).filter(models.Product.product_id == product_id)
    # if not product.first():
    #     return False
    # product.delete(synchronize_session=False)
    # db.commit()
    # return True


def persist_official(store_id: int, official: Official, db: Session = next(get_db())) -> Official:
    """
    persisting a new official to store
    :param db:
    :param store_id: store's id
    :param official: see in Objects
    :return: an updated orm if successful, None otherwise.
    """
    new_official = models.Official(**official.dict(), store_id=store_id)
    db.add(new_official)
    db.commit()
    db.refresh(new_official)
    return new_official


def delete_official(store_id: int, official_username: str, db: Session = next(get_db())) -> bool:
    """
    delete an official from store
    :param db:
    :param store_id: store's id
    :param official_username: the official username
    :return: True if successful, False otherwise.
    """
    return delete_(models.Official,
                   models.Official.store_id == store_id and models.Official.username == official_username, db=db)


def persist_shopping_basket(username: str, basket_item: ShoppingBasketItem,
                            db: Session = next(get_db())) -> ShoppingBasketItem:
    """
    persisting a new shopping basket (collecting all baskets into a cart when requested)
    :param db:
    :param username: the username related to the basket
    :param basket_item: see in Objects
    :return: an updated orm if successful, None otherwise.
    """
    new_basket_item = models.ShoppingBasketItem(**basket_item.dict(), username=username)
    db.add(new_basket_item)
    db.commit()
    db.refresh(new_basket_item)
    return new_basket_item


def delete_shopping_basket(username: str, store_id: int, db: Session = next(get_db())) -> bool:
    """
    delete a shopping basket
    :param db:
    :param username: the user's basket
    :param store_id: the related store to the basket
    :return: True if successful, False otherwise.
    """
    return delete_(models.ShoppingBasketItem,
                   models.ShoppingBasketItem.username == username and models.ShoppingBasketItem.store_id == store_id,
                   db=db)


def persist_notification(username: str, msg: str, db: Session = next(get_db())) -> Notification:
    """
    persisting a new notification
    :param db:
    :param username: the user related to the notification
    :param msg: the notification itself
    :return: an updated orm if successful, None otherwise.
    """
    new_notification = models.Notification(username=username, message=msg)
    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)
    return new_notification


def delete_notification(notification_id: int) -> bool:
    """
    delete a notification
    :param notification_id: the notification's id given on persist
    :return: True if successful, False otherwise.
    """
    return delete_(models.Notification, models.Notification.id == id)


def delete_(cls: type, predicate: bool, db: Session = next(get_db())) -> bool:
    instance = db.query(cls).filter(predicate)
    if not instance.first():
        return False
    instance.delete(synchronize_session=False)
    db.commit()
    return True

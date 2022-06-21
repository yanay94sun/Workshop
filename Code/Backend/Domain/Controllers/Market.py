from Code.Backend.Domain.PaymentServiceAdapter import PaymentServiceAdapter
from Code.Backend.Domain.Publisher.NotificationController import NotificationController, Activities
from Code.Backend.Domain.SupplyServiceAdapter import SupplyServiceAdapter

# from Code.Backend.Domain.ShoppingCart import ShoppingCart
from Code.Backend.Domain.MFResponse import Response

from Code.Backend.Service.Objects.PaymentService import PaymentService





class Market:

    def __init__(self):
        self.__admins_ids = None
        self.__admin_pwd = None
        self.__payment_service = None
        self.__supply_service = None
        self.__payment_service_adapter = None
        self.__supply_service_adapter = None
        self.__notification_controller: NotificationController = None

    def init(self, admin_id, admin_pwd, payment_service, supply_service):
        self.__admins_ids = [admin_id]
        self.__admin_pwd = [admin_pwd]
        self.__payment_service = payment_service
        self.__supply_service = supply_service
        self.__payment_service_adapter = PaymentServiceAdapter()
        self.__supply_service_adapter = SupplyServiceAdapter()

        payment_service_res = self.connect_payment_service(payment_service)
        if payment_service_res.error_occurred():
            return payment_service_res
        supply_service_res = self.connect_supply_service(supply_service)
        if supply_service_res.error_occurred():
            return supply_service_res

        return Response(self)

    def contact_payment_service(self, domain_payment_info):
        return self.__payment_service_adapter.pay(domain_payment_info)

    def contact_supply_service(self, supply_info):
        return self.__supply_service_adapter.supply(supply_info)

    def set_notification_controller(self, controller: NotificationController):
        self.__notification_controller = controller

    # def purchase_shop_cart(self, user_id: str, shopping_cat: ShoppingCart):
    #     pass

    def complaint(self, comp):
        pass

    def connect_payment_service(self, payment_service):
        return self.__payment_service_adapter.connect_payment_service(payment_service)

    def connect_supply_service(self, supply_service):
        return self.__supply_service_adapter.connect_supply_service(supply_service)

    def close_store_permanently(self, user_id: str, store_id: str):
        """
        II.6.1
        :param user_id:
        :param store_id:
        :return:
        """
        pass

    def remove_member(self, user_id: str, member_id: str):
        """
        II.6.2
        :param user_id:
        :param member_id:
        :return:
        """
        pass

    def get_all_users_messages_by_admin(self, user_id: str):
        """
        II.6.3.1
        :param user_id:
        :return:
        """
        pass

    def reply_users_messages_by_admin(self, user_id: str, store_id: str, user_contact_info, admin_contact_info):
        """
        II.6.3.2
        :param user_id:
        :param store_id:
        :param user_contact_info:
        :param admin_contact_info:
        :return:
        """
        pass

    # Moved and split into User controller and Shop Controller

    # def get_stores_purchase_history_by_admin(self, user_id: str, store_id=None):
    #     """
    #     II.6.4
    #     :param user_id:
    #     :param store_id:
    #     :return:
    #     """
    #     pass

    def get_system_statistic_by_admin(self, user_id: str):
        """
        II.6.5
        :param user_id:
        :return:
        """
        pass

    def check_if_admin(self,user_id:str):
        return user_id in self.__admins_ids

    def notify_purchase(self, all_baskets, visitor_state_id):
        for basket in all_baskets:
            store_id = basket.get_store()
            product_and_quantities = basket.get_products_and_quantities()
            product_format = [f"{q} {p}" for p, q in product_and_quantities.items()]
            msg = f"{visitor_state_id} purchased {'|'.join(product_format)}"
            self.__notification_controller.notify_all(store_id, Activities.PURCHASE_IN_STORE, msg)

    def notify_activity(self, store_id, activity: Activities, msg):
        self.__notification_controller.notify_all(store_id, activity, msg)

    def register_store(self, store_name, owner_username):
        self.__notification_controller.register_store(store_name, owner_username)

    def subscribe_to_store(self, store_id, new_owner_id):
        [self.__notification_controller.subscribe(new_owner_id, store_id, act) for act in Activities]

    def remove_store_official(self, store_id, remover_username, subject_username):
        self.__notification_controller.notify_all(store_id,
                                                  Activities.OFFICIAL_REMOVED,
                                                  f"{remover_username} discharged {subject_username} from its duties")
        [self.__notification_controller.unsubscribe(subject_username, store_id, act) for act in Activities]



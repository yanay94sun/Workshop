from Code.Backend.Domain.PaymentServiceAdapter import PaymentServiceAdapter
from Code.Backend.Domain.SupplyServiceAdapter import SupplyServiceAdapter

from Code.Backend.Domain.ShoppingCart import ShoppingCart
from Code.Backend.Domain.MFResponse import Response

from Code.Backend.Service.Objects.PaymentService import PaymentService





class Market:

    def __init__(self):
        self.__admin_id = None
        self.__admin_pwd = None
        self.__payment_service = None
        self.__supply_service = None
        self.__payment_service_adapter = None
        self.__supply_service_adapter = None

    def init(self, admin_id, admin_pwd, payment_service, supply_service):
        self.__admin_id = admin_id
        self.__admin_pwd = admin_pwd
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

    def purchase_shop_cart(self, user_id: str, shopping_cat: ShoppingCart):
        pass

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

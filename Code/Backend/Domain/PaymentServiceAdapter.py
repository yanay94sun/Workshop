from Code.Backend.Domain.MFResponse import Response

# importing the requests library
import requests

class PaymentServiceAdapter:
    def __init__(self):
        # Should be URL
        self.__payment_service = None

    def pay(self, domain_payment_info):
        if self.__payment_service is not None:
            PARAMS = {"action_type", "pay"}, \
                     {"card_number", domain_payment_info.card_number},\
                     {"month", domain_payment_info.month}, \
                     {"year", domain_payment_info.year}, \
                     {"holder", domain_payment_info.holder},\
                     {"ccv", domain_payment_info.ccv}, \
                     {"id", domain_payment_info.id}
            # res = self.__payment_service.pay(domain_payment_info.credit_card,
            #                                         domain_payment_info.cvv,
            #                                         domain_payment_info.amount_to_pay)

            r = requests.post(url=self.__payment_service, data=PARAMS)
            data = r.text
            print(data)
            if data != "-1":
                return Response(value=data)
            return Response(msg="Cannot make payment with the service")
        # SHOULD NOT GET HERE
        return Response(msg="Payment Service is not configured")

    def connect_payment_service(self, payment_service):
        PARAMS = {"action_type":"handshake"}
        r = requests.post(url= payment_service, data= PARAMS)
        data = r.text
        if data == "OK":
            self.__payment_service = payment_service
            return Response(value=data)
        # could not make connection, return response with the error
        return Response(msg=data)

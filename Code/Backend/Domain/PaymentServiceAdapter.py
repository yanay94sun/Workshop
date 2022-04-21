from Code.Backend.Domain.MFResponse import Response


class PaymentServiceAdapter:
    def __init__(self):
        self.__payment_service = None

    def pay(self, domain_payment_info):
        if self.__payment_service is not None:
            # TODO add csv and expiration date support
            is_success = self.__payment_service.pay(domain_payment_info.credit_card,
                                                    domain_payment_info.amount_to_pay)
            if is_success:
                return Response(value=is_success)
            return Response(msg="Cannot make payment with the service")
        # SHOULD NOT GET HERE
        return Response(msg="Payment Service is not configured")

    def connect_payment_service(self, payment_service):

        val = payment_service.make_connection()
        if val is not None:
            self.__payment_service = payment_service
            return Response(value=val)
        return Response(msg="Cannot make connection with Payment Service")

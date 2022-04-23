from Code.Backend.Domain.MFResponse import Response


class SupplyServiceAdapter:
    def __init__(self):
        self.__supply_service = None

    def supply(self, domain_supply_info):
        if self.__supply_service is not None:
            is_success = self.__supply_service.supply(domain_supply_info)

            if is_success:
                return Response(value= is_success)
            return Response(msg= "Cannot make supplement with the service")
        # SHOULD NOT GET HERE
        return Response(msg="Supply Service is not configured")

    def connect_supply_service(self, supply_service):

        val = supply_service.make_connection()
        if val is not None:
            self.__supply_service = supply_service
            return Response(value=val)
        return Response(msg="Cannot make connection with Supply Service")

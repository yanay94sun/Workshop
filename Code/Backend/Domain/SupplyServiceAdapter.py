from Code.Backend.Domain.MFResponse import Response
import requests
from requests.exceptions import Timeout


class SupplyServiceAdapter:
    def __init__(self):
        # Should be URL
        self.__supply_service = None

    def supply(self, domain_supply_info):
        if self.__supply_service is not None:
            PARAMS = {"action_type": "supply",
                      "name": domain_supply_info.name,
                      "address": domain_supply_info.address,
                      "city": domain_supply_info.city,
                      "country": domain_supply_info.country,
                      "zip": domain_supply_info.zip,
                      }

            try:
                r = requests.post(url=self.__supply_service, data=PARAMS, timeout=8)
            except Timeout:
                return Response(msg="Request Timeout")
            data = r.text
            if data != "unexpected-output" and 10000 <= int(data) <= 100000:
                return Response(value=data)
            return Response(msg="Cannot make supply with the service")
        # SHOULD NOT GET HERE
        return Response(msg="Supply Service is not configured")

    def connect_supply_service(self, supply_service):

        # val = supply_service.make_connection()
        # if val is not None:
        #     self.__supply_service = supply_service
        #     return Response(value=val)
        # return Response(msg="Cannot make connection with Supply Service")
        PARAMS = {"action_type": "handshake"}
        r = requests.post(url=supply_service, data=PARAMS)
        data = r.text
        if data == "OK":
            self.__supply_service = supply_service
            return Response(value=data)
        # could not make connection, return response with the error
        return Response(msg=data)

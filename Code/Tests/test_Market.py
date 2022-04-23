import unittest
from unittest import TestCase

from Code.Backend.Domain.DomainPaymentInfo import DomainPaymentInfo
from Code.Backend.Domain.Controllers.Market import Market
from Code.Backend.Domain.PaymentServiceAdapter import PaymentServiceAdapter
from Code.Backend.Domain.SupplyServiceAdapter import SupplyServiceAdapter
from Code.Backend.Service.Objects.PackageInfo import PackageInfo
from Code.Backend.Service.Objects.PaymentService import PaymentService
from Code.Backend.Service.Objects.Payment_info import Payment_info
from Code.Backend.Service.Objects.SupplySevice import SupplyService


class TestMarket(TestCase):
    def setUp(self):
        self.payment_service = PaymentService()
        self.supply_service = SupplyService()
        self.payment_info = DomainPaymentInfo(Payment_info(123456789, "yanay", 4580123456789123, 123, 200))
        self.package_info = PackageInfo("yanay", "shemesh", "beer sheva", "123", {"11": 10})
        self.market = Market().init("yanay","123", self.payment_service, self.supply_service).value

# def test_init(self):
    #     self.assertTrue(
    #         (not self.market.init("admin", "123", self.payment_service, self.supply_service).error_occurred()))

    def test_contact_payment_service(self):
        self.assertTrue(not self.market.contact_payment_service(self.payment_info).error_occurred())


    def test_contact_supply_service(self):
        self.assertTrue(not self.market.contact_supply_service(self.package_info).error_occurred())

    def test_connect_payment_service(self):
        self.assertTrue(not self.market.connect_payment_service(self.payment_service).error_occurred())

    def test_connect_supply_service(self):
        self.assertTrue(not self.market.connect_supply_service(self.supply_service).error_occurred())


if __name__ == '__main__':
    unittest.main()

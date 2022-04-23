# from plistlib import Dict
from typing import Dict

from Code.Backend.Domain import ShoppingBasket
from Code.Backend.Domain.DomainDataObjects.ProductPurchaseRequest import ProductPurchaseRequest
from Code.Backend.Domain.MFResponse import Response
from Code.Backend.Domain.ShoppingBasket import ShoppingBasket


class ShoppingCart:
    def __init__(self):
        """

        """
        self.shopping_baskets: Dict[str, ShoppingBasket] = {} # store_id : basket

    def add_product(self, ppr: ProductPurchaseRequest):
        if ppr.store_id not in self.shopping_baskets:
            self.shopping_baskets[ppr.store_id] = ShoppingBasket(ppr.store_id)
        return self.shopping_baskets[ppr.store_id].add_to_basket(ppr.product_id, ppr.quantity)



    def remove_product(self, ppr: ProductPurchaseRequest):
        if ppr.store_id not in self.shopping_baskets:
            return Response.from_error("no basket of given user and store")
        return self.shopping_baskets[ppr.store_id].remove_from_basket(product_id=ppr.product_id, quantity=ppr.quantity)

    def iter_products(self):
        #  generator
        for store_id, basket in self.shopping_baskets.items():
            for product_id, quantity in basket.get_products_and_quantities().items():
                yield ProductPurchaseRequest(store_id, product_id, quantity)
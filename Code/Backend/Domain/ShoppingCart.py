from plistlib import Dict

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
        if ppr.store_ID in self.shopping_baskets:
            self.shopping_baskets[ppr.store_ID].add_to_basket(ppr.product_ID, ppr.quantity)
        else:
            self.shopping_baskets[ppr.store_ID] = ShoppingBasket(ppr.store_ID)


    def remove_product(self, ppr: ProductPurchaseRequest):
        if ppr.store_ID not in self.shopping_baskets:
            return Response.from_error("no basket of given user and store")
        return self.shopping_baskets[ppr.store_ID]\
            .remove_from_basket(self, product_id=ppr.product_ID, quantity=ppr.quantity)

    def iter_products(self):
        #  generator
        for store_id, basket in self.shopping_baskets.items():
            for product_id, quantity in basket.get_products_and_quantities():
                yield ProductPurchaseRequest(store_id, product_id, quantity)
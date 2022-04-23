class ProductPurchaseRequest:
    def __init__(self,
                 store_id,
                 product_id,
                 quantity):
        """
        """
        self.product_id = product_id
        self.store_id = store_id
        self.quantity = quantity

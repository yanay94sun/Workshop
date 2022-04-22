class ProductPurchaseRequest:
    def __init__(self,
                 store_id,
                 product_id,
                 quantity):
        """
        """
        self.product_ID = product_id
        self.store_ID = store_id
        self.quantity = quantity

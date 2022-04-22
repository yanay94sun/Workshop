from Code.Backend.Service.Objects.PackageInfo import PackageInfo


class DomainPackageInfo:
    def __init__(self, package_info: PackageInfo):
        self.costumer_name = package_info.costumer_name
        self.costume_last_name = package_info.costume_last_name
        self.costumer_address = package_info.costumer_address
        self.store_id = package_info.store_id
        self.products_ids_and_quantity = package_info.products_ids_and_quantity

    def get_costumer_name(self):
        return self.costumer_name

    def get_costumer_last_name(self):
        return self.get_costumer_last_name()

    def get_costumer_address(self):
        return self.costumer_address

    def get_store_id(self):
        return self.store_id

    def get_products_ids_and_quantity(self):
        return self.products_ids_and_quantity

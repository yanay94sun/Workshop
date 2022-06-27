from Code.Backend.Service.Objects.PackageInfo import PackageInfo


class DomainPackageInfo:
    def __init__(self, package_info: PackageInfo):
        self.name = package_info.name
        self.address = package_info.address
        self.city = package_info.city
        self.country = package_info.country
        self.zip = package_info.zip

from enums.ProductStatus import ProductStatus


class Product:
    def __init__(self):
        self.name = None
        self.status = ProductStatus.UNCHANGED.value
        self.location = 'inventory'
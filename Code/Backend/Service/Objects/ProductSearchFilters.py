class ProductSearchFilters:
    def __init__(self, text, by_name=True, by_category=None, filter_type=None,
                 filter_value=None):
        self.text = text
        self.by_name = by_name
        self.by_category = by_category
        self.filter_type = filter_type
        self.filter_value = filter_value

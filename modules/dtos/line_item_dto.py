class LineItemDto:
    def __init__(self, item_name, quantity, total, total_tax, na_miejscu_na_wynos):
        assert na_miejscu_na_wynos
        assert isinstance(na_miejscu_na_wynos, list)
        assert all(isinstance(item, str) for item in na_miejscu_na_wynos)

        self.item_name = item_name
        self.quantity = quantity
        self.total = total
        self.total_tax = total_tax
        self.na_miejscu_na_wynos = na_miejscu_na_wynos  # This is now a list/array of values

    def __str__(self):
        order_types = ', '.join(self.na_miejscu_na_wynos)
        return (
            f"\tItem Name: {self.item_name}\n"
            f"\tQuantity: {self.quantity}\n"
            f"\tTotal: {self.total}\n"
            f"\tTotal Tax: {self.total_tax}\n"
            f"\tOrder Types: [{order_types}]"
        )

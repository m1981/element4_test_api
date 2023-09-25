class LineItemDto:
    def __init__(self, item_name, quantity, total, total_tax, is_vat_exempt, na_miejscu_na_wynos):
        self.item_name = item_name
        self.quantity = quantity
        self.total = total
        self.total_tax = total_tax
        self.is_vat_exempt = is_vat_exempt
        self.na_miejscu_na_wynos = na_miejscu_na_wynos


    def __str__(self):
        return (
            f"\tItem Name: {self.item_name}\n"
            f"\tQuantity: {self.quantity}\n"
            f"\tTotal: {self.total}\n"
            f"\tTotal Tax: {self.total_tax}\n"
            f"\tOrder Type: {self.na_miejscu_na_wynos}"
        )
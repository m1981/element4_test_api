class LineItemDto:
    def __init__(self, item_name, quantity, total, total_tax, is_vat_exempt, na_miejscu_na_wynos):
        self.item_name = item_name
        self.quantity = quantity
        self.total = total
        self.total_tax = total_tax
        self.is_vat_exempt = is_vat_exempt
        self.na_miejscu_na_wynos = na_miejscu_na_wynos

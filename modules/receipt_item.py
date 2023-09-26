class ReceiptItem:
    def __init__(self, name, amount, vat_rate, price, measurement_unit, na_miejscu_na_wynos):
        self.name = name
        self.amount = amount
        self.vat_rate = vat_rate
        self.price = price
        self.measurement_unit = measurement_unit
        self.na_miejscu_na_wynos = na_miejscu_na_wynos


class Order:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)
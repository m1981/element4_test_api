class ReceiptItem:
    def __init__(self, name, amount, vat_rate, price, measurement_unit):
        self.name = name
        self.amount = amount
        self.vat_rate = vat_rate
        self.price = price
        self.measurement_unit = measurement_unit


class Order:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)
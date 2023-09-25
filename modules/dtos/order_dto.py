class OrderDto:
    def __init__(self, order_id, status, billing, line_items, date_created, dodatki_do_pizzy):
        self.order_id = order_id
        self.status = status
        self.billing = billing
        self.line_items = line_items
        self.date_created = date_created
        self.dodatki_do_pizzy = dodatki_do_pizzy

class OrderDto:
    def __init__(self, order_id, status, billing, line_items, date_created, dodatki_do_pizzy):
        self.order_id = order_id
        self.status = status
        self.billing = billing
        self.line_items = line_items
        self.date_created = date_created
        self.dodatki_do_pizzy = dodatki_do_pizzy

    def __str__(self):
        line_items_str = "\n\n".join(str(item) for item in self.line_items)
        return (
            f"Order ID: {self.order_id}\n"
            f"Status: {self.status}\n"
            f"Notatki: {self.dodatki_do_pizzy['notatki']}"
            f"Line Items:\n{line_items_str}\n"
            f"Date Created: {self.date_created}\n"
        )
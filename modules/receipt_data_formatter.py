from datetime import datetime
from modules.receipt_item import ReceiptItem, Order

class ReceiptDataFormatter:
    def __init__(self):
        pass

    @staticmethod
    def format_data(order_dto):
        receipt_order = Order()
        vat_id = 2
        receipt_order.NIP = order_dto.billing['nip_do_paragonu']
        receipt_order.order_id = order_dto.order_id
        receipt_order.date_created = datetime.strptime(order_dto.date_created, "%Y-%m-%dT%H:%M:%S")
        receipt_order.phone_number = order_dto.billing['phone']
        receipt_order.na_miejscu_na_wynos = order_dto.line_items[0].na_miejscu_na_wynos if order_dto.line_items else ""
        receipt_order.comments = order_dto.dodatki_do_pizzy['notatki']

        for item_dto in order_dto.line_items:
            total_price = float(item_dto.total) + float(item_dto.total_tax)
            receipt_item = ReceiptItem(item_dto.item_name, item_dto.quantity*100, vat_id, int(total_price*100), 'szt.')
            receipt_order.add_item(receipt_item)

        return receipt_order
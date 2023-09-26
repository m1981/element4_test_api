from modules.dtos.line_item_dto import LineItemDto
from modules.dtos.order_dto import OrderDto

def test_order_dto_init():
    billing = {'payment_method': 'cash', 'payment_method_title': 'Cash on delivery', 'transaction_id': '123'}
    line_items = [LineItemDto('Item1', 1, 15.0, 1.5, ["Na miejscu"])]
    dodatki_do_pizzy = {'notatki': 'extra cheese'}
    order_dto = OrderDto(1, 'processing', billing, line_items, '2022-10-01T00:00:00', dodatki_do_pizzy)

    assert order_dto.order_id == 1
    assert order_dto.status == 'processing'
    assert order_dto.billing == billing
    assert order_dto.line_items == line_items
    assert order_dto.date_created == '2022-10-01T00:00:00'
    assert order_dto.dodatki_do_pizzy == dodatki_do_pizzy

from modules.dtos.order_dto import OrderDto
from modules.dtos.line_item_dto import LineItemDto

class OrderDataTransformer:
    @staticmethod
    def extract_metadata(meta_data_list):
        na_miejscu_na_wynos = []
        for m in meta_data_list:
            if m['key'].startswith('na_miejscu_na_wynos'):
                na_miejscu_na_wynos.append(m['value'])
        return na_miejscu_na_wynos

    @staticmethod
    def transform_to_order_dto(order):
        na_miejscu_na_wynos = OrderDataTransformer.extract_metadata(order['meta_data'])
        line_items_dto = []
        na_miejscu_index = 0
        for item in order['line_items']:
            na_miejscu_na_wynos_for_item = na_miejscu_na_wynos[na_miejscu_index:na_miejscu_index+item['quantity']]
            line_item_dto = LineItemDto(
                item['name'],
                item['quantity'],
                float(item['total'])/item['quantity'],
                float(item['total_tax'])/item['quantity'],
                na_miejscu_na_wynos_for_item
            )
            line_items_dto.append(line_item_dto)
            na_miejscu_index += item['quantity']
        order_dto = OrderDto(order['id'], order['status'], order['billing'], line_items_dto, order['date_created'], order['dodatki_do_pizzy'])
        return order_dto

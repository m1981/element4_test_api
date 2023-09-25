from modules.dtos.order_dto import OrderDto
from modules.dtos.line_item_dto import LineItemDto

class OrderDataTransformer:
    @staticmethod
    def extract_metadata(meta_data_list):
        is_vat_exempt = False
        na_miejscu_na_wynos = None

        for meta_data in meta_data_list:
            if meta_data['key'] == 'is_vat_exempt':
                is_vat_exempt = meta_data['value'] == 'yes'
            elif meta_data['key'].startswith('na_miejscu_na_wynos'):
                na_miejscu_na_wynos = meta_data['value']

        return is_vat_exempt, na_miejscu_na_wynos

    @staticmethod
    def transform_to_order_dto(order):
        line_items_dto = []
        for item in order['line_items']:
            is_vat_exempt, na_miejscu_na_wynos = OrderDataTransformer.extract_metadata(item['meta_data'])
            line_item_dto = LineItemDto(item['name'], item['quantity'], item['total'], item['total_tax'], is_vat_exempt, na_miejscu_na_wynos)
            line_items_dto.append(line_item_dto)

        order_dto = OrderDto(order['id'], order['status'], order['billing'], line_items_dto, order['date_created'], order['dodatki_do_pizzy'])
        return order_dto


from modules.order_data_transformer import OrderDataTransformer

class TestOrderDataTransformer:

    def test_extract_metadata(self):
        meta_data_list = [
            {"key": "is_vat_exempt", "value": "yes"},
            {"key": "na_miejscu_na_wynos", "value": "Na miejscu"}
        ]
        is_vat_exempt, na_miejscu_na_wynos = OrderDataTransformer.extract_metadata(meta_data_list)
        assert is_vat_exempt == True
        assert na_miejscu_na_wynos == "Na miejscu"

    def test_transform_to_order_dto(self):
        order = {
            'id': 1,
            'status': 'processing',
            'billing': { 'payment_method': 'cash', 'payment_method_title': 'Cash on delivery', 'transaction_id': '123' },
            'line_items': [
                {
                    'name': 'Item1',
                    'quantity': 1,
                    'total': 15.0,
                    'total_tax': 1.5,
                    'meta_data': [
                        {"key": "is_vat_exempt", "value": "yes"},
                        {"key": "na_miejscu_na_wynos", "value": "Na miejscu"}
                    ]
                }
            ],
            'date_created': '2022-10-01T00:00:00',
            'dodatki_do_pizzy': {'notatki': 'extra cheese'}
        }
        
        order_dto = OrderDataTransformer.transform_to_order_dto(order)
        assert order_dto.order_id == 1
        assert order_dto.status == 'processing'
        assert order_dto.billing == order['billing']
        assert len(order_dto.line_items) == 1
        assert order_dto.line_items[0].item_name == 'Item1'
        assert order_dto.line_items[0].quantity == 1
        assert order_dto.line_items[0].total == 15.0
        assert order_dto.line_items[0].total_tax == 1.5
        assert order_dto.line_items[0].is_vat_exempt == True
        assert order_dto.line_items[0].na_miejscu_na_wynos == "Na miejscu"
        assert order_dto.date_created == '2022-10-01T00:00:00'
        assert order_dto.dodatki_do_pizzy == order['dodatki_do_pizzy']

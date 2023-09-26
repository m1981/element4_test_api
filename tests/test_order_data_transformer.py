from modules.order_data_transformer import OrderDataTransformer
from modules.dtos.order_dto import OrderDto
from modules.dtos.line_item_dto import LineItemDto

class TestOrderDataTransformer:

    def test_extract_metadata(self):
        transformer = OrderDataTransformer()
        input_data = [
            {"key": "na_miejscu_na_wynos", "value": "Na miejscu"},
            {"key": "na_miejscu_na_wynos_2", "value": "Na wynos"},
        ]
        got_na_miejscu_na_wynos = transformer.extract_metadata(input_data)

        assert got_na_miejscu_na_wynos == {1: 'Na miejscu', 2: 'Na wynos'}


    def test_transform_to_order_dto(self):
        order_data = {
            "id": 2854,
            "status": "completed",
            "billing": {
                "first_name": "Test",
                "last_name": "User",
                "address_1": "123 Test St",
                "address_2": "",
                "city": "Testville",
                "postcode": "12345",
                "country": "Testland",
                "phone": "1234567890"
            },
            "line_items": [
                {
                    "name": "Test Product 1",
                    "quantity": 1,
                    "total": "10.00",
                    "total_tax": "1.00",
                    "meta_data": [
                        {
                            "key": "is_vat_exempt",
                            "value": "no"
                        }
                    ]
                },
                {
                    "name": "Test Product 2",
                    "quantity": 2,
                    "total": "20.00",
                    "total_tax": "2.00",
                    "meta_data": [
                        {
                            "key": "is_vat_exempt",
                            "value": "no"
                        }
                    ]
                }
            ],
            "meta_data": [
                {
                    "id": 37759,
                    "key": "is_vat_exempt",
                    "value": "no"
                },
                {
                    "id": 37763,
                    "key": "na_miejscu_na_wynos",
                    "value": "Na miejscu"
                },
                {
                    "id": 37764,
                    "key": "na_miejscu_na_wynos_2",
                    "value": "Na wynos"
                },
            ],
            "date_created": "2021-08-01T00:00:00",
            "dodatki_do_pizzy": {
                "dodatki_do_pizzy_popup": "",
                "dodatki_do_sniadan": "",
                "info_zamowienia": "",
                "notatki": ""
            }
        }

        order_dto = OrderDataTransformer.transform_to_order_dto(order_data)

        # Assertions to ensure that the transformation happened correctly
        assert isinstance(order_dto, OrderDto)
        assert order_dto.order_id == order_data['id']
        assert order_dto.status == order_data['status']
        assert order_dto.billing == order_data['billing']

        # Assert the transformation inside line items
        assert len(order_dto.line_items) == len(order_data['line_items'])

        for index, line_item in enumerate(order_dto.line_items):
            assert isinstance(line_item, LineItemDto)
            assert line_item.item_name == order_data['line_items'][index]['name']
            assert line_item.quantity == order_data['line_items'][index]['quantity']
            assert line_item.total == float(order_data['line_items'][index]['total'])/line_item.quantity
            assert line_item.total_tax == float(order_data['line_items'][index]['total_tax'])/line_item.quantity
            assert line_item.na_miejscu_na_wynos == order_data['meta_data'][index + 1]['value']


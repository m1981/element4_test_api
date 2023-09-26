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

        assert got_na_miejscu_na_wynos == ['Na miejscu', 'Na wynos']


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
                {
                    "id": 37764,
                    "key": "na_miejscu_na_wynos_2",
                    "value": "Na miejscu"
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

        assert order_dto.line_items[0].na_miejscu_na_wynos == ['Na miejscu']
        assert order_dto.line_items[1].na_miejscu_na_wynos == ['Na wynos', 'Na miejscu']



    def test_transform_to_order_dto2(self):
        order_data = {
  "_links": {
    "collection": [
      {
        "href": "https://fabrykasmakow.com.pl/wp-json/wc/v3/orders"
      }
    ],
    "self": [
      {
        "href": "https://fabrykasmakow.com.pl/wp-json/wc/v3/orders/2715"
      }
    ]
  },
  "date_created": "2021-08-01T00:00:00",
  "billing": {
    "czy_chce_nip": "",
    "first_name": "Anna",
    "nip_do_paragonu": "",
    "phone": "503755544",
  },
  "cart_hash": "7c59c091421f595c8818729f2b28f7cc",
  "dodatki_do_pizzy": {
    "dodatki_do_pizzy_popup": "",
    "dodatki_do_sniadan": "",
    "info_zamowienia": "",
    "notatki": "Danie DNIA na miejscu, reszta na wynos"
  },
  "fee_lines": [],
  "id": 2715,
  "line_items": [
    {
      "id": 917,
      "name": "Makaron dnia",
      "price": 16.666666666666668,
      "product_id": 2117,
      "quantity": 3,
      "subtotal": "50.00",
      "subtotal_tax": "4.00",
      "total": "50.00",
      "total_tax": "4.00",
      "variation_id": 0
    },
    {
      "id": 918,
      "name": "Risotto z kurkami",
      "price": 14.814815,
      "product_id": 1663,
      "quantity": 1,
      "subtotal": "14.81",
      "subtotal_tax": "1.19",
      "total": "14.81",
      "total_tax": "1.19",
      "variation_id": 0
    },
    {
      "id": 919,
      "name": "Danie Dnia",
      "price": 12.962963,
      "product_id": 2120,
      "quantity": 1,
      "sku": "",
      "subtotal": "12.96",
      "subtotal_tax": "1.04",
      "total": "12.96",
      "total_tax": "1.04",
      "variation_id": 0
    }
  ],
  "meta_data": [
    {
      "id": 33996,
      "key": "is_vat_exempt",
      "value": "no"
    },
    {
      "id": 33997,
      "key": "_thwcfe_ship_to_billing",
      "value": "1"
    },
    {
      "id": 33998,
      "key": "_thwcfe_disabled_fields",
      "value": "nip_do_paragonu"
    },
    {
      "id": 33999,
      "key": "na_miejscu_na_wynos",
      "value": "Na wynos"
    },
    {
      "id": 33999,
      "key": "na_miejscu_na_wynos_2",
      "value": "Na wynos"
    },
        {
      "id": 33999,
      "key": "na_miejscu_na_wynos_3",
      "value": "Na wynos"
    },
    {
      "id": 33999,
      "key": "na_miejscu_na_wynos_4",
      "value": "Na miejscu"
    },
    {
      "id": 33999,
      "key": "na_miejscu_na_wynos_5",
      "value": "Na wynos"
    },
    {
      "id": 34000,
      "key": "notatki",
      "value": "Danie DNIA na miejscu, reszta na wynos"
    },
    {
      "id": 34002,
      "key": "_payu_order_status",
      "value": "COMPLETED|CBNP6VTV9Q230919GUEST000P01"
    }
  ],
  "status": "processing",
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

        print(order_dto.line_items[0])
        assert order_dto.line_items[0].na_miejscu_na_wynos == ['Na wynos', 'Na wynos', 'Na wynos']
        assert order_dto.line_items[1].na_miejscu_na_wynos == ['Na miejscu']
        assert order_dto.line_items[2].na_miejscu_na_wynos == ['Na wynos']


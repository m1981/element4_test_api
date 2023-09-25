from _datetime import datetime
from modules.receipt_data_formatter import ReceiptDataFormatter
from modules.order_data_transformer import OrderDataTransformer

def test_create_receipt_order():
    # Arrange
    order = {
        'billing': {
            'nip_do_paragonu': '1234567890', 
            'phone': '1234567890'
        },
        'id': '1',
        "status": "processing",
        'date_created': f"{datetime.now():%Y-%m-%dT%H:%M:%S}", 
        'line_items': [
            {'name': "item1", 'quantity': 5, 'total': "10.0", 'total_tax': "0.5", 'na_miejscu_na_wynos': "Yes"},
            {'name': "item2", 'quantity': 2, 'total': "20.0", 'total_tax': "1.0", 'na_miejscu_na_wynos': "No"},
        ],
        'dodatki_do_pizzy': {
            'notatki': 'Test comment'
        },
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
      "id": 34000,
      "key": "notatki",
      "value": "Danie DNIA na miejscu, reszta na wynos"
    },
    {
      "id": 34002,
      "key": "_payu_order_status",
      "value": "COMPLETED|CBNP6VTV9Q230919GUEST000P01"
    }
  ]
    }

    order_dto = OrderDataTransformer.transform_to_order_dto(order)
    expected_nip = order_dto.billing['nip_do_paragonu']
    expected_phone_number = order_dto.billing['phone']
    expected_order_id = order_dto.order_id
    expected_comments = order_dto.dodatki_do_pizzy['notatki']

    # Act
    result = ReceiptDataFormatter.format_data(order_dto)

    # Assert
    assert result.NIP == expected_nip
    assert result.phone_number == expected_phone_number
    assert result.order_id == expected_order_id
    assert result.comments == expected_comments
    assert len(result.items) == len(order_dto.line_items)
    assert result.items[0].name == order_dto.line_items[0].item_name

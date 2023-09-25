import unittest

from modules.treeview_data_formatter import TreeViewDataFormatter
from modules.dtos.order_dto import OrderDto
from modules.dtos.line_item_dto import LineItemDto

class TestFormatDataForDisplay(unittest.TestCase):
    def setUp(self):
        pass

    def test_format_data_for_display(self):
        # Prepare data for the test
        line_item_1 = LineItemDto("Test Product 1", 1, "10.00", "1.00", False, "Na miejscu")
        line_item_2 = LineItemDto("Test Product 2", 2, "20.00", "2.00", False, "Na wynos")
        order_dto = OrderDto(2854, "completed", {}, [line_item_1, line_item_2], "", "")
        
        # Method under test
        result = TreeViewDataFormatter.format_data_for_display(order_dto)
        
        # Check result
        expected_result = [
            ('Test Product 1', 1, '11.00 PLN'),
            ('Test Product 2', 2, '22.00 PLN')
        ]
        self.assertEqual(result, expected_result)
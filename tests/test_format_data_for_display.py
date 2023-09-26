import unittest

from modules.treeview_data_formatter import TreeViewDataFormatter
from modules.dtos.order_dto import OrderDto
from modules.dtos.line_item_dto import LineItemDto

class TestFormatDataForDisplay(unittest.TestCase):
    def setUp(self):
        pass

    def test_format_data_for_display(self):
        # Prepare data for the test
        line_item_1 = LineItemDto("Test Product 1", 1, "10.00", "1.00", "Na miejscu")
        line_item_2 = LineItemDto("Test Product 2", 2, "20.00", "2.00", "Na wynos")
        order_dto = OrderDto(2854, "completed", {}, [line_item_1, line_item_2], "", "")
        
        # Method under test
        result = TreeViewDataFormatter.format_data_for_display(order_dto)
        
        # Check result
        expected_result = [
            ('Test Product 1', 1, "Na miejscu", '11.00 PLN'),
            ('Test Product 2', 2, "Na wynos", '44.00 PLN')
        ]
        self.assertEqual(result, expected_result)


    def test_format_data_for_display2(self):
        # Prepare data for the test
        line_item_1 = LineItemDto("Makaron dnia", 3, 16.666666666666668, 1.3333, "Na wynos")
        line_item_2 = LineItemDto("Risotto z kurkami", 1, 14.814815, 1.19,  "Na wynos")
        line_item_3 = LineItemDto("Danie Dnia", 1, 12.962963, 1.04,  "Na miejscu")
        order_dto = OrderDto(2715, "processing", {}, [line_item_1, line_item_2, line_item_3], "", "Danie DNIA na miejscu, reszta na wynos")

        # Method under test
        result = TreeViewDataFormatter.format_data_for_display(order_dto)

        # Check result
        expected_result = [
            ('Makaron dnia', 3, 'Na wynos', '54.00 PLN'),
            ('Risotto z kurkami', 1, 'Na wynos', '16.00 PLN'),
            ('Danie Dnia', 1, 'Na miejscu', '14.00 PLN'),
        ]
        self.assertEqual(result, expected_result)
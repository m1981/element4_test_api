import json
import unittest
from modules.order_data_transformer import OrderDataTransformer

class TestOrderDataTransformerJson(unittest.TestCase):
    def setUp(self):
        # Load the test data from test_order_1.json
        with open('tests/test_data/test_order_1.json') as f:
            self.order_1 = json.load(f)

        # Load the test data from test_order_2715.json
        with open('tests/test_data/test_order_2715.json') as f:
            self.order_2715 = json.load(f)

    def test_extract_metadata(self):
        # Apply the extraction method to the test data and assert the expected results
        na_miejscu_na_wynos_1 = OrderDataTransformer.extract_metadata(self.order_1['meta_data'])
        self.assertEqual(na_miejscu_na_wynos_1, ['Na miejscu', 'Na wynos'])

    def test_extract_metadata_2715(self):
        na_miejscu_na_wynos_2 = OrderDataTransformer.extract_metadata(self.order_2715['meta_data'])
        self.assertEqual(na_miejscu_na_wynos_2,
        ['Na wynos', 'Na wynos', 'Na miejscu', 'Na wynos', 'Na miejscu'])
    #
    def test_wynos_per_instance_in_line_item_2715(self):
        # Apply the transformation method to the test data and assert the expected results.
        order_dto = OrderDataTransformer.transform_to_order_dto(self.order_2715)
        self.assertEqual(order_dto.line_items[0].na_miejscu_na_wynos, ['Na wynos', 'Na wynos', 'Na miejscu'])
        self.assertEqual(order_dto.line_items[1].na_miejscu_na_wynos, ['Na wynos'])
        self.assertEqual(order_dto.line_items[2].na_miejscu_na_wynos, ['Na miejscu'])

if __name__ == '__main__':
    unittest.main()

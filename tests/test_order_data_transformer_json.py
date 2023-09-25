import json
import unittest
from modules.order_data_transformer import OrderDataTransformer

class TestOrderDataTransformerJson(unittest.TestCase):
    def setUp(self):
        # Load the test data from test_order_1.json
        with open('tests/test_data/test_order_1.json') as f:
            self.order_1 = json.load(f)

        # Load the test data from test_order_2.json
        # with open('test_data/test_order_2.json') as f:
        #     self.order_2 = json.load(f)

    def test_extract_metadata(self):
        # Apply the extraction method to the test data and assert the expected results
        is_vat_exempt_1, na_miejscu_na_wynos_1 = OrderDataTransformer.extract_metadata(self.order_1['meta_data'])
        self.assertEqual(is_vat_exempt_1, False)
        self.assertEqual(na_miejscu_na_wynos_1, {1: 'Na miejscu', 2: 'Na wynos'})
        
        # Repeat for the second test file
        # is_vat_exempt_2, na_miejscu_na_wynos_2 = OrderDataTransformer.extract_metadata(self.order_2['meta_data'])
        # self.assertEqual(is_vat_exempt_2, False)
        # self.assertEqual(na_miejscu_na_wynos_2, {1: 'Na miejscu', 2: 'Na wynos'})
    #
    def test_transform_to_order_dto(self):
        # Apply the transformation method to the test data and assert the expected results.
        order_dto_1 = OrderDataTransformer.transform_to_order_dto(self.order_1)
        self.assertEqual(order_dto_1.status, 'processing')
    #
    #     # Repeat for the second test file
    #     order_dto_2 = OrderDataTransformer.transform_to_order_dto(self.order_2)
    #     self.assertEqual(order_dto_2.status, 'processing')

if __name__ == '__main__':
    unittest.main()

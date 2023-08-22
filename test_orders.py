import unittest
from unittest.mock import patch, MagicMock
from orders_receiver import OrderManager
from itertools import cycle


class MockResponse:
    def __init__(self, json_data):
        self.json_data = json_data
    def json(self):
        return self.json_data

class TestOrderHandling(unittest.TestCase):
    def setUp(self):
        self.manager = OrderManager()

    def test_order_fetching_sequence(self):
        self.manager.process_status = 'processing'
        mock_orders = [
            {'id': '1', 'status': 'completed'},
            {'id': '2', 'status': 'processing'},
            {'id': '3', 'status': 'processing'},
            {'id': '4', 'status': 'completed'}
        ]

        with patch('requests.get') as mock_get, patch('requests.put') as mock_put:
            # make requests.get() return a new list every time
            mock_get.side_effect = lambda *args, **kwargs: MockResponse(json_data=list(mock_orders))
            mock_put.side_effect = lambda *args, **kwargs: mock_orders[1].update({"status": "completed"})
            # Fetch the next order, it should be the first 'processing' order
            self.manager.update_order()
            self.assertEqual(self.manager.order_id, '2')

            # Simulate completing this order
            self.manager.change_order_status(self.manager.order_id, 'completed')

            # Fetch the next order, it should be the second 'processing' order
            self.manager.update_order()
            self.assertEqual(self.manager.order_id, '3')


if __name__ == '__main__':
    unittest.main()

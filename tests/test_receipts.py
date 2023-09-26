from modules.mock_printer import MockPrinter
from receipt import Printer
from modules.receipt_item import ReceiptItem, Order
from modules.receipt_data_formatter import ReceiptDataFormatter
from modules.dtos.line_item_dto import LineItemDto
from modules.dtos.order_dto import OrderDto

def test_print_order_items(capfd):
    mock_printer = MockPrinter()  # MockPrinter instance

    # Prepare the test Order

    # Call the method
    # Prepare data for the test
    line_item_1 = LineItemDto("Makaron dnia", 1, "10.00", "1.00", ["Na miejscu 1"])
    line_item_2 = LineItemDto("Risotto z kurkami", 2, "20.00", "2.00", ["Na wynos 2", "Na miejscu 3"])
    order_dto = OrderDto(2854, "completed", {'nip_do_paragonu': '', 'phone': '123123123'}, [line_item_1, line_item_2], "2023-09-19T13:11:14", {'notatki': ''})

    order_formated = ReceiptDataFormatter.format_data(order_dto)


    printer = Printer(1, 1, 1, 1, True)
    printer.print_order_items(order_formated, mock_printer)

    # Capture output
    out, err = capfd.readouterr()

    # Prepare the expected output:
    expected_output = "{}\t{}\n".format('10', "")
    expected_output += "{}\t{}\n".format('40', "Makaron dnia")
    expected_output += "{}\t{}\n".format('40', "1.0")
    expected_output += "{}\t{}\n".format('40', "Na miejscu 1")
    expected_output += "{}\t{}\n".format('10', "")
    expected_output += "{}\t{}\n".format('40', "Risotto z kurkami")
    expected_output += "{}\t{}\n".format('40', "2.0")
    expected_output += "{}\t{}\n".format('40', "Na wynos 2")
    expected_output += "{}\t{}\n".format('40', "Na miejscu 3")

    # Compare the captured output with the expected output
    assert out == expected_output


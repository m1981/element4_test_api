import ctypes
from base64 import b64encode
import requests
import winsound
import threading
from operator import itemgetter


elzabdr = ctypes.CDLL('./elzabdr.dll')


# Declare function arguments and types
elzabdr.CommunicationInit.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
elzabdr.CommunicationInit.restype = ctypes.c_int

elzabdr.pFillLines.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)]
elzabdr.pFillLines.restype = ctypes.c_int

elzabdr.pFillPayment.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
elzabdr.pFillPayment.restype = ctypes.c_int

elzabdr.ReceiptBegin.restype = ctypes.c_int

elzabdr.PackageItem.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
elzabdr.PackageItem.restype = ctypes.c_int

elzabdr.pReceiptItemEx.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                   ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
elzabdr.pReceiptItemEx.restype = ctypes.c_int

elzabdr.ReceiptEnd.argtypes = [ctypes.c_int]
elzabdr.ReceiptEnd.restype = ctypes.c_int

elzabdr.CommunicationEnd.restype = ctypes.c_int

elzabdr.pErrMessage.argtypes = [ctypes.c_int, ctypes.c_char_p]
elzabdr.pErrMessage.restype = ctypes.c_int

elzabdr.pNonFiscalPrintoutLine.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
elzabdr.pNonFiscalPrintoutLine.restype = ctypes.c_int


class ReceiptItem:
    def __init__(self, item):
        self.name = item['name']  # set product name
        self.amount = item['quantity']  # set quantity
        self.vat_rate = 'vat_rate'  # take from the `line_items` if provided
        self.price = float(item['total']) + float(item['total_tax'])  # Total Price including Tax
        self.measurement_unit = 'szt.'  # not directly available, set a default or based on business rules

class Order:
    def __init__(self, json_order):
        self.items = [ReceiptItem(item) for item in json_order['line_items']]
        self.czy_chce_nip = True
        self.NIP = json_order.get('billing', {}).get('nip_do_paragonu', "default_value")  # <- Default value set here if not found
        self.order_id = json_order.get('id', "default_value")
        self.phone_number = json_order.get('billing', {}).get('phone', "default_value")
        self.na_miejscu_na_wynos = json_order.get('billing', {}).get('na_miejscu_na_wynos', "default_value")
        self.comments = json_order.get('dodatki_do_pizzy', {}).get('notatki', "default_value")


class Printer:
    def __init__(self, elzabdr, port, speed, timeout):
        self.elzabdr = elzabdr
        self.port = port
        self.speed = speed
        self.timeout = timeout

    def print_receipt(self, order):
        W = ctypes.c_int()
        OpisBledu = ctypes.create_string_buffer(255)
        if self.elzabdr.CommunicationInit(self.port, self.speed, self.timeout) != 0:
            raise Exception('Cannot init printer')
        try:
            self.elzabdr.pFillLines(2, "Sklep internetowy".encode('utf-8'), ctypes.byref(W))

            elzabdr.pReceiptPurchaserNIP(order.NIP.encode('utf-8'))
            elzabdr.ReceiptBegin()

            for item in order.items:
                elzabdr.pReceiptItemEx(1, item.name.encode('utf-8'), item.vat_rate, 0, item.amount, 2,item.measurement_unit.encode('utf-8'),item.price)
            elzabdr.ReceiptEnd(0)
        finally:
            if self.elzabdr.CommunicationEnd() != 0:
                raise Exception('Cannot end printer communication')

    def print_internal_order(self, order):
        W = ctypes.c_int()
        OpisBledu = ctypes.create_string_buffer(255)

        if self.elzabdr.CommunicationInit(self.port, self.speed, self.timeout) != 0:
            raise Exception('Cannot init printer')



    def print_internal_order(self, order):
        try:
            W = ctypes.c_int()
            OpisBledu = ctypes.create_string_buffer(255)
            if self.elzabdr.CommunicationInit(self.port, self.speed, self.timeout) != 0:
                raise Exception('Cannot init printer')

            self.elzabdr.NonFiscalPrintoutBegin(53)
            self.elzabdr.pNonFiscalPrintoutLine(10, b"", 0)

            for item in order.items:
                self.elzabdr.pNonFiscalPrintoutLine(40, item.name.encode('utf-8'), 1)
                self.elzabdr.pNonFiscalPrintoutLine(40, str(item.amount/100).encode('utf-8'), 1)

            # Zapisz zamownienie do pliku
            # Zwieksz numer zamowienia
            message = "Numer kolejny: {}".format(str(order.order_id))
            self.elzabdr.pNonFiscalPrintoutLine(1, message.encode('utf-8'), 1)

            self.elzabdr.pNonFiscalPrintoutLine(1, str(order.na_miejscu_na_wynos).encode('utf-8'), 1)
            # Max line length is 36 characters
            self.elzabdr.pNonFiscalPrintoutLine(1, str(order.comments).encode('utf-8'), 1)
            self.elzabdr.pNonFiscalPrintoutLine(11, b"Telefon", 1)
            # Print EAN code
            self.elzabdr.pNonFiscalPrintoutLine(21, str(order.phone_number).encode('utf-8'), 1);
            #
            self.elzabdr.NonFiscalPrintoutEnd()
            wynik = self.elzabdr.CommunicationEnd()
            if wynik == 0:
                print("Program zakończony bezbłędnie")
        finally:
          self.elzabdr.CommunicationEnd()

if __name__ == "__main__":
    printer = Printer(elzabdr, 1, 9600, 5)
    order = Order()
    order.add_item(ReceiptItem('TowarTestowy_A', 200, 1, 150, 'szt.'))
    order.add_item(ReceiptItem('TowarTestowy_B', 100, 1, 250, 'szt.'))
    printer.print_receipt(order)
    printer.print_internal_order(order)

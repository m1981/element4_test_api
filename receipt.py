import ctypes

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
    def __init__(self, name, amount, vat_rate, price, item_type, measurement_unit):
        self.name = name
        self.amount = amount
        self.vat_rate = vat_rate
        self.price = price
        self.item_type = item_type
        self.measurement_unit = measurement_unit


class Order:
    def __init__(self, shop_name, NIP):
        self.items = []
        self.shop_name = shop_name
        self.NIP = NIP

    def add_item(self, item):
        self.items.append(item)


class Printer:
    def __init__(self, elzabdr, port, speed, timeout):
        self.elzabdr = elzabdr
        self.port = port
        self.speed = speed
        self.timeout = timeout

    def init(self):
        if self.elzabdr.CommunicationInit(self.port, self.speed, self.timeout) != 0:
            raise Exception('Cannot init printer')

    def end(self):
        if self.elzabdr.CommunicationEnd() != 0:
            raise Exception('Cannot end printer communication')

    def print_receipt(self, order):
        try:
            self.init()
            W = ctypes.c_int()
            OpisBledu = ctypes.create_string_buffer(255)
            self.elzabdr.pFillLines(2, order.shop_name.encode('utf-8'), ctypes.byref(W))
            if W.value != 0:
                elzabdr.pErrMessage(W.value, OpisBledu)
                print('Error:', OpisBledu.value)
                return
            elzabdr.pReceiptPurchaserNIP(order.NIP.encode('utf-8'))
            elzabdr.ReceiptBegin()

            for item in order.items:
                elzabdr.pReceiptItemEx(1, item.name.encode('utf-8'), item.amount, 0, item.price, item.vat_rate, item.measurement_unit.encode('utf-8'))
                if W.value != 0:
                    elzabdr.pErrMessage(W.value, OpisBledu)
                    print('Error:', OpisBledu.value)
                    return
            elzabdr.ReceiptEnd(0)
        finally:
            self.end()


    def print_internal_order(self, order):
        try:
            self.init()
            for item in order.items:
                self.elzabdr.NonFiscalPrintoutBegin(53)
                self.elzabdr.pNonFiscalPrintoutLine(10, b"", 0)
                self.elzabdr.pNonFiscalPrintoutLine(40, b"TowarTestowy_A", 1)
                self.elzabdr.pNonFiscalPrintoutLine(40, b"TowarTestowy_B", 1)

                self.elzabdr.pNonFiscalPrintoutLine(1, b"Numer kolejny: 34", 1)
                self.elzabdr.pNonFiscalPrintoutLine(1, b"Wynos", 1)
                # Max line length is 36 characters
                self.elzabdr.pNonFiscalPrintoutLine(1, "Bez boczku i mięsa bo jeste weganin".encode('utf-8'), 1)
                self.elzabdr.pNonFiscalPrintoutLine(1, "em. Poprosze ekstra sałatę i na godzię 12:00".encode('utf-8'), 1)
                self.elzabdr.pNonFiscalPrintoutLine(11, b"Telefon", 1)

            # Zapisz zamownienie do pliku
            # Zwieksz numer zamowienia

            # Print EAN code
            self.elzabdr.pNonFiscalPrintoutLine(21, b"791630003", 1);
            #
            self.elzabdr.NonFiscalPrintoutEnd()
            if wynik == 0:
                print("Program zakończony bezbłędnie")
        finally:
            self.end()

if __name__ == "__main__":
    # Setting up the printer
    printer = Printer(elzabdr, 2, 9600, 5)

    # Creating an order
    order = Order('Sklep internetowy', '1234567890')

    # Adding items
    order.add_item(ReceiptItem('TowarTestowy_A', 1, 0, 100, 2, 'szt.'))
    order.add_item(ReceiptItem('TowarTestowy_B', 1, 0, 100, 2, 'szt.'))

    # Printing
    printer.print_receipt(order)

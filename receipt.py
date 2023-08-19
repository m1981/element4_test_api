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

    def print_receipt(self, order):
        W = ctypes.c_int()
        OpisBledu = ctypes.create_string_buffer(255)
        print('receipt')
        if self.elzabdr.CommunicationInit(2, 9600, 5) != 0:
            raise Exception('Cannot init printer')
        print(self.port)
        try:
            self.elzabdr.pFillLines(2, "Sklep internetowy".encode('utf-8'), ctypes.byref(W))

            elzabdr.pReceiptPurchaserNIP(order.NIP.encode('utf-8'))
            print("asdas")
            elzabdr.ReceiptBegin()
            print("Begin")

            for item in order.items:
                 if (str6 == "23")
                                pReceiptItemEx(1, Nazwa, 1, 0, 100, 2, "szt.", Cena);
                            if (str6 == "5")
                                pReceiptItemEx(1, Nazwa, 3, 0, 100, 2, "szt.", Cena);
                            if (str6 == "8")
                                pReceiptItemEx(1, Nazwa, 2, 0, 100, 2, "szt.", Cena);
w = elzabdr.pReceiptItemEx(1, b"TowarTestowy_A", 1, 0, 100, 2, b"szt.", 150)
                elzabdr.pReceiptItemEx(1, item.name.encode('utf-8'), item.amount, 0, item.price, item.vat_rate, item.measurement_unit.encode('utf-8'))
                if W.value != 0:
                    elzabdr.pErrMessage(W.value, OpisBledu)
                    print('Error:', OpisBledu.value)
                    return
            elzabdr.ReceiptEnd(0)
        finally:
            if self.elzabdr.CommunicationEnd() != 0:
                raise Exception('Cannot end printer communication')

    def print_internal_order(self, order):
        W = ctypes.c_int()
        OpisBledu = ctypes.create_string_buffer(255)

        if self.elzabdr.CommunicationInit(self.port, self.speed, self.timeout) != 0:
            raise Exception('Cannot init printer')


if __name__ == "__main__":
    printer = Printer(elzabdr, 2, 9600, 5)
    order = Order('Sklep internetowy', '1234567890')
    order.add_item(ReceiptItem('TowarTestowy_A', 1, 0, 100, 2, 'szt.'))
    order.add_item(ReceiptItem('TowarTestowy_B', 1, 0, 100, 2, 'szt.'))
    printer.print_receipt(order)
    #printer.print_internal_order(order)

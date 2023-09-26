import ctypes
from modules.mock_printer import MockPrinter



class PrintException(Exception):
    pass


class Printer:
    BEGIN_PRINTOUT = 53
    LINE_ITEM = 40
    PHONE_NUMBER = 21
    TELEFON_FIELD = 11
    ORDER_DETAILS = 1
    EMPTY_LINE = 10
    NEW_LINE = 1
    NO_NEW_LINE = 0

    def __init__(self, elzabdr, port, speed, timeout, local, init_dll=True):
        self.elzabdr = elzabdr
        self.port = port
        self.speed = speed
        self.timeout = timeout
        self.local = local

    def initilize_dll(self):
        # Declare function arguments and types
        self.elzabdr.CommunicationInit.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
        self.elzabdr.CommunicationInit.restype = ctypes.c_int

        self.elzabdr.pFillLines.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)]
        self.elzabdr.pFillLines.restype = ctypes.c_int

        self.elzabdr.pFillPayment.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
        self.elzabdr.pFillPayment.restype = ctypes.c_int

        self.elzabdr.ReceiptBegin.restype = ctypes.c_int

        self.elzabdr.PackageItem.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
        self.elzabdr.PackageItem.restype = ctypes.c_int

        self.elzabdr.pReceiptItemEx.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                           ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
        self.elzabdr.pReceiptItemEx.restype = ctypes.c_int

        self.elzabdr.ReceiptEnd.argtypes = [ctypes.c_int]
        self.elzabdr.ReceiptEnd.restype = ctypes.c_int

        self.elzabdr.CommunicationEnd.restype = ctypes.c_int

        self.elzabdr.pErrMessage.argtypes = [ctypes.c_int, ctypes.c_char_p]
        self.elzabdr.pErrMessage.restype = ctypes.c_int

        self.elzabdr.pNonFiscalPrintoutLine.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
        self.elzabdr.pNonFiscalPrintoutLine.restype = ctypes.c_int

    def print_receipt(self, order):
        if self.local:
            self.local_print_receipt(order)
        else:
            W = ctypes.c_int()
            OpisBledu = ctypes.create_string_buffer(255)
            if self.elzabdr.CommunicationInit(self.port, self.speed, self.timeout) != 0:
                raise Exception('Cannot init printer')
            try:
                self.elzabdr.pFillLines(2, "Sklep internetowy".encode('windows-1250'), ctypes.byref(W))

                elzabdr.pReceiptPurchaserNIP(order.NIP.encode('windows-1250'))
                elzabdr.ReceiptBegin()

                for item in order.items:
                    elzabdr.pReceiptItemEx(1, item.name.encode('windows-1250'), item.vat_rate, 0, item.amount, 2,item.measurement_unit.encode('windows-1250'),item.price)
                elzabdr.ReceiptEnd(0)
            finally:
                if self.elzabdr.CommunicationEnd() != 0:
                    raise Exception('Cannot end printer communication')



    def print_internal_order(self, order, elzabdr, W=ctypes.c_int(), OpisBledu=ctypes.create_string_buffer(255)):
        if self.local:
            elzabdr = MockPrinter()

        try:
            if elzabdr.CommunicationInit(self.port, self.speed, self.timeout) != 0:
                raise PrintException("Cannot init printer")
            elzabdr.NonFiscalPrintoutBegin(self.BEGIN_PRINTOUT )
            elzabdr.pNonFiscalPrintoutLine(self.EMPTY_LINE , b"", self.NO_NEW_LINE)
            self.print_order_items(order, elzabdr)
            self.print_order_details(order, elzabdr)
            elzabdr.NonFiscalPrintoutEnd()
            wynik = elzabdr.CommunicationEnd()
        except Exception as e:
            self.handle_exception(e)
        finally:
                elzabdr.CommunicationEnd()

    def print_order_items(self, order, elzabdr):
        for item in order.items:
            elzabdr.pNonFiscalPrintoutLine(self.EMPTY_LINE , b"", self.NO_NEW_LINE)
            elzabdr.pNonFiscalPrintoutLine(self.LINE_ITEM, item.name.encode('windows-1250'), self.NEW_LINE)
            elzabdr.pNonFiscalPrintoutLine(self.LINE_ITEM, str(item.amount/100).encode('windows-1250'), self.NEW_LINE)
            for placing in item.na_miejscu_na_wynos:
                elzabdr.pNonFiscalPrintoutLine(self.LINE_ITEM, placing.encode('windows-1250'), self.NEW_LINE)

    def print_order_details(self, order, elzabdr):
        message = "Numer kolejny: {}".format(str(order.order_id)[-3:])
        elzabdr.pNonFiscalPrintoutLine(self.EMPTY_LINE , b"", self.NO_NEW_LINE)
        elzabdr.pNonFiscalPrintoutLine(self.ORDER_DETAILS, message.encode('windows-1250'), self.NEW_LINE)
        elzabdr.pNonFiscalPrintoutLine(self.ORDER_DETAILS, str(order.comments).encode('windows-1250'), self.NEW_LINE)
        elzabdr.pNonFiscalPrintoutLine(self.TELEFON_FIELD, b"Telefon", self.NEW_LINE)
        elzabdr.pNonFiscalPrintoutLine(self.PHONE_NUMBER, str(order.phone_number).encode('windows-1250'), self.NEW_LINE)

    def local_print_receipt(self, order):
        print('--- Receipt ---')
        print('Store: Sklep internetowy')
        print('NIP: ', order.NIP)
        print('Data online: ', order.date_created.strftime("%d-%m %H:%M"))
        for item in order.items:
            print(item.name, item.vat_rate, 0, item.amount, 2,item.measurement_unit, item.price)
        print('\n')

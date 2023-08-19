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


def print_receipt(elzabdr):
    W = ctypes.c_int()
    OpisBledu = ctypes.create_string_buffer(255)
    Port = 1
    Szybkosc = 9600
    Timeout = 5
    wynik = elzabdr.CommunicationInit(Port, Szybkosc, Timeout)
    if wynik == 0:
        wynik = elzabdr.pFillLines(2, "Sklep internetowy".encode('utf-8'), ctypes.byref(W))
        if wynik == 0:
                # jezeli wybrano NIP to wydrukuj NIP
                elzabdr.pReceiptPurchaserNIP(b"1234567890")

                wynik = elzabdr.ReceiptBegin()
                if wynik == 0:
                    wynik = elzabdr.pReceiptItemEx(1, b"TowarTestowy_A", 1, 0, 100, 2, b"szt.", 150)
                    if wynik == 0:
                        wynik = elzabdr.pReceiptItemEx(1, b"TowarTestowy_B", 1, 0, 100, 2, b"szt.", 250)
                        if wynik == 0:
                            wynik = elzabdr.ReceiptEnd(0)
                            if wynik == 0:
                                wynik = elzabdr.CommunicationEnd()
                                if wynik == 0:
                                    print("Program zakończony bezbłędnie")
                                    return 0
    # był błąd
    elzabdr.pErrMessage(wynik, OpisBledu)
    print(OpisBledu.value)

def print_internal_order(elzabdr):
    W = ctypes.c_int()
    OpisBledu = ctypes.create_string_buffer(255)
    Port = 1
    Szybkosc = 9600
    Timeout = 5

    wynik = elzabdr.CommunicationInit(Port, Szybkosc, Timeout)
    if wynik != 0:
        print("Blad inicjalizacji")
        return 1
    elzabdr.NonFiscalPrintoutBegin(53)
    elzabdr.pNonFiscalPrintoutLine(10, b"", 0)
    elzabdr.pNonFiscalPrintoutLine(40, b"TowarTestowy_A", 1)
    elzabdr.pNonFiscalPrintoutLine(40, b"TowarTestowy_B", 1)

    elzabdr.pNonFiscalPrintoutLine(1, b"Numer kolejny: 34", 1)
    elzabdr.pNonFiscalPrintoutLine(1, b"Wynos", 1)
    # Max line length is 36 characters
    elzabdr.pNonFiscalPrintoutLine(1, "Bez boczku i mięsa bo jeste weganin".encode('utf-8'), 1)
    elzabdr.pNonFiscalPrintoutLine(1, "em. Poprosze ekstra sałatę i na godzię 12:00".encode('utf-8'), 1)
    elzabdr.pNonFiscalPrintoutLine(11, b"Telefon", 1)

    # Zapisz zamownienie do pliku
    # Zwieksz numer zamowienia

    # Print EAN code
    elzabdr.pNonFiscalPrintoutLine(21, b"791630003", 1);
    #
    elzabdr.NonFiscalPrintoutEnd()
    wynik = elzabdr.CommunicationEnd()
    if wynik == 0:
        print("Program zakończony bezbłędnie")
if __name__ == "__main__":
    #print_receipt(elzabdr)
    print_internal_order(elzabdr)

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


# Application Logic
def main():
    W = ctypes.c_int()
    OpisBledu = ctypes.create_string_buffer(255)
    Port = 1
    Szybkosc = 9600
    Timeout = 5

    wynik = elzabdr.CommunicationInit(Port, Szybkosc, Timeout)
    if wynik == 0:
        wynik = elzabdr.pFillLines(2, "gotówka".encode('utf-8'), ctypes.byref(W))
        if wynik == 0:
            wynik = elzabdr.pFillPayment(1, "gotówka".encode('utf-8'), 150000, 1763)
            if wynik == 0:
                wynik = elzabdr.ReceiptBegin()
                if wynik == 0:
                    wynik = elzabdr.pReceiptItemEx(1, b"TowarTestowy_A", 1, 0, 100, 2, b"szt.", 150)
                    if wynik == 0:
                        wynik = elzabdr.pReceiptItemEx(1, b"TowarTestowy_B", 1, 0, 100, 2, b"szt.", 250)
                        if wynik == 0:
                            wynik = elzabdr.ReceiptEnd(5)
                            if wynik == 0:
                                wynik = elzabdr.CommunicationEnd()
                                if wynik == 0:
                                    print("Program zakończony bezbłędnie")
                                    return 0
    # był błąd
    elzabdr.pErrMessage(wynik, OpisBledu)
    print(OpisBledu.value)


if __name__ == "__main__":
    main()

class MockPrinter:
    def __init__(self):
        pass

    def pNonFiscalPrintoutLine(self, arg1, arg2, arg3):
        print(f"{arg1}\t{arg2.decode('windows-1250')}")

    def CommunicationInit(self, port, speed, timeout):
        return 0

    def NonFiscalPrintoutBegin(self, param):
        pass

    def NonFiscalPrintoutEnd(self):
        pass

    def CommunicationEnd(self):
        pass
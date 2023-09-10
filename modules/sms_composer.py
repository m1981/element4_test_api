import time

class SMSComposer:
    WAIT_TIME = 1

    def __init__(self, connection):
        self._connection = connection

    def compose_sms(self, phone_number, message):
        self._write_with_pause('AT+CMGF=1\r')
        self._write_with_pause(f'AT+CMGS="{phone_number}"\r')
        self._write_with_pause(f'{message}\r')

    def _write_with_pause(self, text):
        time.sleep(self.WAIT_TIME)
        self._connection.write(text.encode())
        time.sleep(self.WAIT_TIME)

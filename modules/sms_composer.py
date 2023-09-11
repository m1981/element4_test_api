import time
import re

class InvalidPhoneNumberException(Exception):
    pass

class SMSComposer:
    WAIT_TIME = 1

    def __init__(self, connection):
        self._connection = connection

    def compose_sms(self, phone_number, message):
        print("compose_sms {} {}".format(phone_number, message))
        print("port: " + self._connection.port)
        if self._is_valid_number(phone_number):
            phone_number = "+48" + phone_number
            self._write_with_pause(b'AT+CMGF=1\r')
            self._write_with_pause(b'AT+CMGS="' + phone_number.encode() + b'"\r')
            self._write_with_pause(message.encode() + b"\r")
        else:
            raise InvalidPhoneNumberException("Invalid phone number. It should be 9 digits long.")

    def _write_with_pause(self, text):
        print("_write_with_pause: {}".format(text))
        self._connection.write(text)
        time.sleep(self.WAIT_TIME)

    @staticmethod
    def _is_valid_number(number: str) -> bool:  # added phone number validation check
        return bool(re.match(r'\d{9}', number))
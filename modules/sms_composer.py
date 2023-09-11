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
        if self._is_valid_number(phone_number):
            self._write_with_pause('AT+CMGF=1\r')
            self._write_with_pause(f'AT+CMGS="+48{phone_number}"\r') # Added the '+48' prefix to the phone number
            self._write_with_pause(f'{message}\r')
        else:
            raise InvalidPhoneNumberException("Invalid phone number. It should be 9 digits long.")

    def _write_with_pause(self, text):
        time.sleep(self.WAIT_TIME)
        print("_write_with_pause: {}".format(text))
        self._connection.write(text.encode())
        time.sleep(self.WAIT_TIME)

    @staticmethod
    def _is_valid_number(number: str) -> bool:  # added phone number validation check
        return bool(re.match(r'\d{9}', number))
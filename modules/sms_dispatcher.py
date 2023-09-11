import logging

class SMSDispatcher:
    def __init__(self, composer):
        self._composer = composer

    def reset_modem(self):
        print("reset modem")
        self._composer._write_with_pause(b'ATZ\r')

    def send_sms(self, phone_number, message):
        print("send_sms")
        try:
            self.reset_modem()
            self._composer.compose_sms(phone_number, message)
            self._composer._write_with_pause(bytes(26))
            print("Message sent successfully!")
        except Exception as e:
            logging.error(f"Error occurred while sending SMS: {str(e)}")
            raise

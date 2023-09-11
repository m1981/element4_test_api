import logging

class SMSDispatcher:
    def __init__(self, composer):
        self._composer = composer

    def reset_modem(self):
        self._composer._write_with_pause('ATZ\r')

    def send_sms(self, phone_number, message):
        try:
            self.reset_modem()
            self._composer.compose_sms(phone_number, message)
            self._composer._write_with_pause(chr(26))
            logging.info("Message sent successfully!")
        except Exception as e:
            logging.error(f"Error occurred while sending SMS: {str(e)}")
            raise

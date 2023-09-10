import argparse
import logging
import re
from modules.serial_connection import SerialConnection
from modules.sms_composer import SMSComposer
from modules.sms_dispatcher import SMSDispatcher

logging.basicConfig(level=logging.INFO)

def main(scanner_port, sms_port):
    PHONE_NUMBER_PATTERN = r'\d{9}'
    establish_connection = SerialConnection()
    scanner_connection = establish_connection.create_serial_connection(scanner_port)
    composer = SMSComposer(establish_connection.create_serial_connection(sms_port))
    dispatcher = SMSDispatcher(composer)

    while scanner_connection.isOpen():
        barcode_data = scanner_connection.readline().decode('utf-8').strip()
        if re.match(PHONE_NUMBER_PATTERN, barcode_data):
            dispatcher.send_sms("+48" + barcode_data, "Your meal is ready for pickup :)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scanner and SMS sender application.')
    parser.add_argument('scanner_port', type=str, help='The scanner serial port')
    parser.add_argument('sms_port', type=str, help='The SMS sender serial port')
    args = parser.parse_args()
    main(args.scanner_port, args.sms_port)

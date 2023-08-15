import serial
import time
import re
import argparse

class RB900ModemAdapter:
    def __init__(self, port, baudrate = 9600, timeout = 5):
        while True:
            try:
                self.ser = serial.Serial(port, baudrate, timeout=timeout)
                break
            except (serial.SerialException, FileNotFoundError):
                print("Nie można otworzyć portu '{0}'. Upewnij się, że jest poprawny i nie jest już używany".format(port))
                time.sleep(5)

    def send_sms(self, phone_number, message):
        try:
            self.ser.write(b'ATZ\r')
            time.sleep(1)
            self.ser.write(b'AT+CMGF=1\r')
            time.sleep(1)
            self.ser.write(b'AT+CMGS="' + phone_number.encode() + b'"\r')
            time.sleep(1)
            self.ser.write(message.encode() + b"\r")
            time.sleep(1)
            self.ser.write(bytes([26]))
            time.sleep(1)
        except Exception as e:
            print("Nie udało się wysłać SMS-a: ", str(e))

    def __del__(self):
        if self.ser is not None:
            try:
                self.ser.close()
                print("Zamknięto połączenie szeregowe.")
            except Exception as e:
                print("Nie udało się zamknąć połączenia szeregowego: ", str(e))

def main(scanner_port, sms_port):
    while True:
        try:
            ser = serial.Serial(scanner_port, baudrate=9600, parity='N', stopbits=1, bytesize=8, timeout=1)
        except (serial.SerialException, FileNotFoundError):
            print(f"Nie można otworzyć portu {scanner_port}. Upewnij się, że jest poprawny i nie jest już używany")
            time.sleep(5)
        else:
            break

    modem = RB900ModemAdapter(port=sms_port)

    if ser.isOpen():
        print("Połączenie szeregowe jest otwarte. Gotowe do odczytu.")
        while True:
            try:
                print("Skanowanie...")
                barcode_data = ser.readline().decode('utf-8').strip()
                if len(barcode_data) > 0:
                    if re.match(r'\d{9}', barcode_data):
                        phone_number = '+48' + barcode_data
                        message = "Danie gotowe do odbioru, zapraszamy :)"
                        modem.send_sms(phone_number, message)
                        print("Wiadomość wysłana pomyślnie!")
                    else:
                        print("Nieprawidłowy numer telefonu. Powinien składać się z 9 cyfr.")
            except KeyboardInterrupt:
                ser.close()
                print("Połączenie szeregowe zamknięte")
                break
    else:
        print("Nie można otworzyć połączenia szeregowego.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scanner and SMS sender application.')
    parser.add_argument('scanner_port', type=str, help='The scanner serial port')
    parser.add_argument('sms_port', type=str, help='The SMS sending serial port')
    args = parser.parse_args()
    main(args.scanner_port, args.sms_port)

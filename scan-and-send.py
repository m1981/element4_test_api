import serial
import time
import re

class RB900ModemAdapter:
    def __init__(self, port='COM12', baudrate = 9600, timeout = 5):
        while True:
            try:
                self.ser = serial.Serial(port, baudrate, timeout=timeout)
                break
            except (serial.SerialException, FileNotFoundError):
                print("Nie mo?na otworzy? portu '{0}'. Upewnij si?, ?e jest poprawny i nie jest ju? u?ywany".format(port))
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
            print("Nie uda?o si? wys?a? SMS-a: ", str(e))

    def __del__(self):
        if self.ser is not None:
            try:
                self.ser.close()
                print("Zamkni?to po??czenie szeregowe.")
            except Exception as e:
                print("Nie uda?o si? zamkn?? po??czenia szeregowego: ", str(e))

def main():
    while True:
        try:
            # Specify your COM Port and Baud Rate accordingly here.
            ser = serial.Serial('COM10', baudrate=9600, parity='N', stopbits=1, bytesize=8, timeout=1)
        except (serial.SerialException, FileNotFoundError):
            print("Nie mo?na otworzy? portu 'COM10'. Upewnij si?, ?e jest poprawny i nie jest ju? u?ywany")
            time.sleep(5)
        else:
            break

    modem = RB900ModemAdapter()

    # Make sure serial connection is open
    if ser.isOpen():
        print("Po??czenie szeregowe jest otwarte. Gotowe do odczytu.")
        while True:
            try:
                print("Skanowanie...")
                barcode_data = ser.readline().decode('utf-8').strip()
                if len(barcode_data) > 0:
                    if re.match(r'\d{9}', barcode_data):
                        phone_number = '+48' + barcode_data
                        message = "Danie gotowe :)"
                        modem.send_sms(phone_number, message)
                        print("Wiadomo?? wys?ana pomy?lnie!")
                    else:
                        print("Nieprawid?owy numer telefonu. Powinien sk?ada? si? z 9 cyfr.")
            except KeyboardInterrupt:
                ser.close()
                print("Po??czenie szeregowe zamkni?te")
                break
    else:
        print("Nie mo?na otworzy? po??czenia szeregowego.")

if __name__ == "__main__":
    main()

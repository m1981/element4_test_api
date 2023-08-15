import serial
import time

class RB900ModemAdapter:
    def __init__(self, port='COM4', baudrate = 9600, timeout = 5):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
    def send_sms(self, phone_number, message):
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

    def __del__(self):
        if self.ser is not None:
            self.ser.close()

def main():
    modem = RB900ModemAdapter()

    phone_number = '+48519687702'
    message = input("Message: ")

    modem.send_sms(phone_number, message)

    print("Message sent successfully!")

if __name__ == "__main__":
    main()

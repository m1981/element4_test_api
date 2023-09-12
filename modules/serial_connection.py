import serial
import logging

class SerialConnection:
    BAUDRATE = 9600

    def create_serial_connection(self, port):
        try:
            connection = serial.Serial(port, self.BAUDRATE, parity='N', stopbits=1, bytesize=8, timeout=2)
        except serial.SerialException as e:
            logging.error(f'Error occurred while connecting to {port}: {str(e)}')
            raise
        else:
            return connection

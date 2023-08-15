import serial

# Specify your COM Port and Baud Rate accordingly here.
ser = serial.Serial('COM10', baudrate=9600, parity='N', stopbits=1, bytesize=8, timeout=1)

# Make sure serial connection is open
if ser.isOpen():
    print("Serial connection is open. Ready to read.")
    try:
        while True:
            print("Scanning...")
            barcode_data = ser.readline().decode('utf-8').strip()
            print("You scanned: ", barcode_data)
    except KeyboardInterrupt:
        ser.close()
        print("Serial connection closed")
else:
    print("Cannot open serial connection.")

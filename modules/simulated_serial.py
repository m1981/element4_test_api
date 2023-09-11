class SimulatedSerialConnection:
    def create_serial_connection(self, _):
        print("Simulated Serial connection created.")
        return self

    def write(self, message):
        print(f"Simulated write: {message}")

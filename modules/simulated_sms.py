# modules/simulated_sms.py

class SimulatedSMSComposer:

    def compose_sms(self, phone_number, message):
        print(f"Simulated SMS composed to {phone_number} with message: {message}")


class SimulatedSMSDispatcher:

    def __init__(self, composer):
        self._composer = composer

    def send_sms(self, phone_number, message):
        self._composer.compose_sms(phone_number, message)
        print("Simulated SMS sent successfully!")


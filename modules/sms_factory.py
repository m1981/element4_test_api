# modules/sms_factory.py
from modules.sms_composer import SMSComposer
from modules.sms_dispatcher import SMSDispatcher
from modules.serial_connection import SerialConnection
from modules.simulated_serial import SimulatedSerialConnection
from modules.simulated_sms import SimulatedSMSComposer
from modules.simulated_sms import SimulatedSMSDispatcher

class SmsFactory:
    @staticmethod
    def get_composer(connection):
        pass

    @staticmethod
    def get_dispatcher(composer):
        pass


class RealSmsFactory(SmsFactory):
    @staticmethod
    def get_connection(port):
        return SerialConnection().create_serial_connection(port)

    @staticmethod
    def get_composer(connection):
        return SMSComposer(connection)

    @staticmethod
    def get_dispatcher(composer):
        return SMSDispatcher(composer)


class SimulatedSmsFactory(SmsFactory):
    @staticmethod
    def get_connection(_):
        return SimulatedSerialConnection().create_serial_connection(_)

    @staticmethod
    def get_composer(_):
        return SimulatedSMSComposer()

    @staticmethod
    def get_dispatcher(_):
        composer = SimulatedSmsFactory.get_composer(_)
        return SimulatedSMSDispatcher(composer)


import pytest
from serial import Serial, SerialException
from unittest.mock import MagicMock, patch
from modules.serial_connection import SerialConnection

@pytest.fixture
def mock_serial_connection():
    return MagicMock(spec=Serial)  # replace this with the actual function

def test_create_serial_connection(mock_serial_connection):
    # Setup - Define port and replace the serial.Serial with a mock
    port = 'mock_port'
    with patch('modules.serial_connection.serial.Serial', return_value=mock_serial_connection) as mock_serial:

        # Exercise - Create a serial connection
        serial_con = SerialConnection()
        con = serial_con.create_serial_connection(port)

        # Verify - Assert that serial.Serial was called with the correct port
        mock_serial.assert_called_once_with(port, SerialConnection.BAUDRATE)

        # Verify - Assert the return value (connection) is correct
        assert con == mock_serial_connection

def test_create_serial_connection_exception():
    # Setup - Define port and set serial.Serial to raise an exception
    port = 'invalid_port'
    with patch('modules.serial_connection.serial.Serial', side_effect=SerialException('Connection error')):

        # Exercise - Create a serial connection and assert that it raises an exception
        serial_con = SerialConnection()
        with pytest.raises(SerialException):
            serial_con.create_serial_connection(port)

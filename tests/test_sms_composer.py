import pytest
from unittest.mock import MagicMock, patch, call
from modules.sms_composer import SMSComposer
from modules.sms_dispatcher import SMSDispatcher

def test_compose_sms(mock_sms_composer):
    # Setup - Define phone number and message values
    phone_number = '123456789'
    message = 'Test message'

    # Exercise - Call the compose_sms method
    with patch.object(mock_sms_composer, '_write_with_pause') as mock_write_with_pause:
        mock_sms_composer.compose_sms(phone_number, message)

    # Verify - Assert that the _write_with_pause method was called with correct parameters
    calls = [call('AT+CMGF=1\r'), call(f'AT+CMGS="{phone_number}"\r'), call(f'{message}\r')]
    mock_write_with_pause.assert_has_calls(calls)


def test_send_sms_while_another_being_sent(mock_sms_composer):
    dispatcher = SMSDispatcher(mock_sms_composer)
    with patch('modules.sms_composer.SMSComposer._write_with_pause',
               side_effect=[None, Exception("Port busy")]), patch('logging.error') as mock_logger:
        try:
            dispatcher.send_sms('1234567890', 'test message')
            dispatcher.send_sms('1234567890', 'test message')
        except Exception:
            pass
        assert mock_logger.called

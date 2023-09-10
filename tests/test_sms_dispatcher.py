import pytest
from unittest.mock import MagicMock, patch, call
from modules.sms_dispatcher import SMSDispatcher


def test_send_sms(fixture_sms_dispatcher):
    # Setup - Define phone number
    phone_number = '123456789'
    message = 'Test message'

    # Mock the compose_sms and _write_with_pause methods
    with patch.object(fixture_sms_dispatcher._composer, 'compose_sms') as mock_compose:
        with patch.object(fixture_sms_dispatcher._composer, '_write_with_pause') as mock_write:

            # Call the send_sms method
            fixture_sms_dispatcher.send_sms(phone_number, message)

            # Assert that compose_sms was called once with correct arguments
            mock_compose.assert_called_once_with(phone_number, message)

            # Assert that _write_with_pause was called once with the correct argument
            mock_write.assert_called_once_with(chr(26))




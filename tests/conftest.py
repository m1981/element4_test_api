import os
import pytest
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from unittest.mock import MagicMock
from modules.sms_composer import SMSComposer
from modules.sms_dispatcher import SMSDispatcher

@pytest.fixture
def mock_sms_composer():
    return SMSComposer(MagicMock())

@pytest.fixture
def fixture_sms_dispatcher(mock_sms_composer):
    return SMSDispatcher(mock_sms_composer)

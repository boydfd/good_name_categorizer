from unittest import TestCase
from unittest.mock import MagicMock

from utilities import retry_for_exception, retry_for_exception_decorator


class UtilitiesTest(TestCase):
    def test_retryForException_whenThrowException_shouldRetry(self):
        mock = MagicMock()

        def call():
            raise KeyError

        mock.side_effect = call

        try:
            retry_for_exception(KeyError, mock, 10)
        except Exception as e:
            self.assertIsInstance(e, KeyError)
        self.assertEquals(10, mock.call_count)

    def test_retryForExceptionDecorator_whenThrowException_shouldRetry(self):
        mock = MagicMock()

        def call():
            raise KeyError

        mock.side_effect = call
        mock_with_decorator = retry_for_exception_decorator(KeyError, 10)(mock)

        try:
            mock_with_decorator()
        except Exception as e:
            self.assertIsInstance(e, KeyError)
        self.assertEquals(10, mock.call_count)

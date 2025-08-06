from unittest.mock import patch
from notifications.services import email_service, sms_service, telegram_service


class TestEmailService:
    @patch("django.core.mail.send_mail")
    def test_send_email_success(self, mock_send):
        mock_send.return_value = 1
        recipient = type("Recipient", (), {"email": "test@example.com"})
        success, error = email_service.send_email(recipient, "Test")
        assert success is True
        assert error is None


class TestSMSService:
    @patch("requests.post")
    def test_send_sms_success(self, mock_post):
        mock_post.return_value.json.return_value = {"status": "OK", "id": "123"}
        recipient = type("Recipient", (), {"phone_number": "79991234567"})
        success, error = sms_service.send_sms(recipient, "Test")
        assert success is True
        assert "123" in error


class TestTelegramService:
    @patch("requests.post")
    def test_send_telegram_success(self, mock_post):
        mock_post.return_value.status_code = 200
        recipient = type("Recipient", (), {"telegram_id": "123"})
        success, error = telegram_service.send_telegram(recipient, "Test")
        assert success is True
        assert error is None

import pytest
from unittest.mock import patch
from notifications.models import Notification, Recipient
from notifications.tasks import send_notification_task, send_via_channel


@pytest.mark.django_db
class TestTasks:
    @pytest.fixture
    def notification(self):
        recipient = Recipient.objects.create(email="test@example.com")
        return Notification.objects.create(recipient=recipient, message="Test")

    @patch("notifications.tasks.send_via_channel.delay")
    def test_send_notification_task(self, mock_send, notification):
        send_notification_task(notification.id)
        mock_send.assert_called_once_with(notification.id, "email", ["email"])

    @patch("notifications.services.email_service.send_email")
    def test_send_via_channel_email(self, mock_send, notification):
        mock_send.return_value = (True, None)
        result = send_via_channel(notification.id, "email", ["email"])
        assert result == "success"

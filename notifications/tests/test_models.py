import pytest
from notifications.models import Recipient, Notification, DeliveryAttempt
from django.utils import timezone


@pytest.mark.django_db
class TestModels:
    @pytest.fixture
    def recipient(self):
        return Recipient.objects.create(
            email="test@example.com",
            phone_number="79991234567",
            telegram_id="123456789",
        )

    @pytest.fixture
    def notification(self, recipient):
        return Notification.objects.create(
            recipient=recipient,
            message="Test message",
        )

    def test_recipient_str(self, recipient):
        assert str(recipient) == "test@example.com"
        recipient.email = None
        assert str(recipient) == "79991234567"

    def test_notification_str(self, notification):
        assert "test@example.com" in str(notification)

    def test_delivery_attempt_str(self, notification):
        attempt = DeliveryAttempt.objects.create(
            notification=notification,
            channel="sms",
            status="sent",
            sent_at=timezone.now(),
        )
        assert "SMS" in str(attempt)
        assert "test@example.com" in str(attempt)

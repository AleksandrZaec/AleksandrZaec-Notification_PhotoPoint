import pytest
from notifications.models import Recipient, Notification, DeliveryAttempt


@pytest.fixture
def recipient():
    return Recipient.objects.create(
        email="fixture@example.com",
        phone_number="79997654321",
        telegram_id="987654321",
    )


@pytest.fixture
def notification(recipient):
    return Notification.objects.create(
        recipient=recipient,
        message="Fixture message",
    )


@pytest.fixture
def delivery_attempt(notification):
    return DeliveryAttempt.objects.create(
        notification=notification,
        channel="email",
        status="sent",
    )

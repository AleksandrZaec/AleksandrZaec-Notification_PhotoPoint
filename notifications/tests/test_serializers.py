import pytest
from notifications.serializers import RecipientSerializer, NotificationSerializer


@pytest.mark.django_db
class TestRecipientSerializer:
    @pytest.mark.parametrize("data, is_valid", [
        ({"email": "valid@example.com"}, True),
        ({"phone_number": "79991234567"}, True),
        ({"phone_number": "invalid"}, False),
        ({}, False),
    ])
    def test_validation(self, data, is_valid):
        serializer = RecipientSerializer(data=data)
        assert serializer.is_valid() == is_valid


@pytest.mark.django_db
class TestNotificationSerializer:
    def test_create_notification(self):
        data = {
            "recipients": [{"email": "new@example.com"}],
            "message": "Hello",
        }
        serializer = NotificationSerializer(data=data)
        assert serializer.is_valid()
        notifications = serializer.save()
        assert len(notifications) == 1
        assert notifications[0].recipient.email == "new@example.com"

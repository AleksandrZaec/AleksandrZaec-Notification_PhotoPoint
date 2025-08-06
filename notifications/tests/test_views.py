import pytest
from rest_framework.test import APIClient
from notifications.models import Recipient


@pytest.mark.django_db
class TestNotificationAPI:
    @pytest.fixture
    def client(self):
        return APIClient()

    def test_create_notification(self, client):
        data = {
            "recipients": [{"email": "api_test@example.com"}],
            "message": "API Test",
        }
        response = client.post("/api/notifications/", data, format="json")
        assert response.status_code == 201
        assert Recipient.objects.filter(email="api_test@example.com").exists()

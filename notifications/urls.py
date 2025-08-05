from django.urls import path
from .views import NotificationCreateAPIView

urlpatterns = [
    path('notifications/', NotificationCreateAPIView.as_view(), name='notification-send'),
]

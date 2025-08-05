from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from notifications.serializers import NotificationSerializer
from notifications.tasks import send_notification_task


class NotificationCreateAPIView(APIView):
    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        notifications = serializer.save()

        for notification in notifications:
            send_notification_task.delay(notification.id)

        return Response(
            {"created_notifications": len(notifications)},
            status=status.HTTP_201_CREATED
        )

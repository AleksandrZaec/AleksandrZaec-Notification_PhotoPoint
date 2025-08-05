from rest_framework import serializers
from notifications.models import Recipient, Notification, DeliveryAttempt
import phonenumbers
import re


class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = ['email', 'phone_number', 'telegram_id']

    def validate(self, data):
        email = data.get('email')
        phone = data.get('phone_number')
        telegram_id = data.get('telegram_id')

        if not (email or phone or telegram_id):
            raise serializers.ValidationError("At least one contact field must be provided.")

        if phone:
            try:
                parsed_phone = phonenumbers.parse(phone, "RU")
                if not phonenumbers.is_valid_number(parsed_phone):
                    raise serializers.ValidationError({"phone_number": "Invalid phone number."})
            except phonenumbers.NumberParseException:
                raise serializers.ValidationError({"phone_number": "Invalid phone number format."})

        if telegram_id:
            if not re.fullmatch(r'\d+', telegram_id):
                raise serializers.ValidationError({"telegram_id": "Telegram ID must be digits only."})

        return data


class BulkNotificationListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        notifications = []

        for item in validated_data:
            recipients_data = item.pop('recipients')
            message = item.get('message')

            final_recipients = []
            for rd in recipients_data:
                recipient = None
                if rd.get('email'):
                    recipient = Recipient.objects.filter(email=rd['email']).first()
                if not recipient and rd.get('phone_number'):
                    recipient = Recipient.objects.filter(phone_number=rd['phone_number']).first()
                if not recipient and rd.get('telegram_id'):
                    recipient = Recipient.objects.filter(telegram_id=rd['telegram_id']).first()

                if not recipient:
                    recipient = Recipient.objects.create(**rd)

                final_recipients.append(recipient)

            notifications.extend([
                Notification(recipient=recipient, message=message)
                for recipient in final_recipients
            ])

        return Notification.objects.bulk_create(notifications)


class NotificationSerializer(serializers.ModelSerializer):
    recipients = RecipientSerializer(many=True)

    class Meta:
        model = Notification
        fields = ['id', 'recipients', 'message']
        list_serializer_class = BulkNotificationListSerializer

    def create(self, validated_data):
        recipients_data = validated_data.pop('recipients')
        message = validated_data.get('message')

        final_recipients = []
        for rd in recipients_data:
            recipient = None
            if rd.get('email'):
                recipient = Recipient.objects.filter(email=rd['email']).first()
            if not recipient and rd.get('phone_number'):
                recipient = Recipient.objects.filter(phone_number=rd['phone_number']).first()
            if not recipient and rd.get('telegram_id'):
                recipient = Recipient.objects.filter(telegram_id=rd['telegram_id']).first()

            if not recipient:
                recipient = Recipient.objects.create(**rd)

            final_recipients.append(recipient)

        notifications = [
            Notification(recipient=recipient, message=message)
            for recipient in final_recipients
        ]

        return Notification.objects.bulk_create(notifications)


class DeliveryAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAttempt
        fields = ['notification', 'channel', 'status', 'error_message']

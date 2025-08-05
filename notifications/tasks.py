from celery import shared_task
from django.utils import timezone
from notifications.models import Notification, DeliveryAttempt
from notifications.services.email_service import send_email
from notifications.services.sms_service import send_sms
from notifications.services.telegram_service import send_telegram
import logging

logger = logging.getLogger(__name__)

CHANNELS = [
    ('email', send_email),
    ('sms', send_sms),
    ('telegram', send_telegram),
]


def get_available_channels(recipient):
    available = []

    for channel_name, _ in CHANNELS:
        if (channel_name == 'email' and recipient.email) or \
                (channel_name == 'sms' and recipient.phone_number) or \
                (channel_name == 'telegram' and recipient.telegram_id):
            available.append(channel_name)

    return available

@shared_task
def send_notification_task(notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
    except Notification.DoesNotExist:
        logger.error(f"Notification {notification_id} does not exist")
        return

    recipient = notification.recipient
    available_channels = get_available_channels(recipient)

    if not available_channels:
        logger.error(f"No available channels for recipient {recipient.id}")
        return

    first_channel = available_channels[0]
    send_via_channel.delay(notification_id, first_channel, available_channels)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_via_channel(self, notification_id, channel_name, available_channels):
    try:
        notification = Notification.objects.get(id=notification_id)
    except Notification.DoesNotExist:
        logger.error(f"Notification {notification_id} does not exist")
        return

    recipient = notification.recipient
    message = notification.message
    send_func = dict(CHANNELS)[channel_name]

    logger.info(f"Attempting to send notification {notification_id} via {channel_name} to recipient {recipient}")

    try:
        success, error = send_func(recipient, message)
    except Exception as e:
        logger.error(f"Error sending via {channel_name}: {str(e)}")
        success, error = False, str(e)

    DeliveryAttempt.objects.create(
        notification=notification,
        channel=channel_name,
        status='sent' if success else 'failed',
        sent_at=timezone.now(),
        error_message=error if not success else None,
    )

    if success:
        logger.info(f"Notification {notification_id} successfully sent via {channel_name}")
        return 'success'

    logger.warning(f"Failed to send notification {notification_id} via {channel_name}: {error}")

    try:
        current_index = available_channels.index(channel_name)
        next_channel = available_channels[current_index + 1] if current_index + 1 < len(available_channels) else None

        if next_channel:
            logger.info(f"Trying next channel {next_channel} for notification {notification_id}")
            return send_via_channel.delay(notification_id, next_channel, available_channels)

        logger.error(f"No more channels left for notification {notification_id}")
        return 'failed'

    except ValueError:
        logger.error(f"Channel {channel_name} not in available channels list")
        return 'failed'

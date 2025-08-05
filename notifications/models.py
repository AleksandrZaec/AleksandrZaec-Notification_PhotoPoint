from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Recipient(models.Model):
    email = models.EmailField(**NULLABLE)
    phone_number = models.CharField(max_length=20, **NULLABLE)
    telegram_id = models.CharField(max_length=100, **NULLABLE)

    def __str__(self):
        return self.email or self.phone_number or self.telegram_id or "Unknown"


class Notification(models.Model):
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification to {self.recipient}"


class DeliveryAttempt(models.Model):
    CHANNEL_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('telegram', 'Telegram'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]

    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='attempts')
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    sent_at = models.DateTimeField(**NULLABLE)
    error_message = models.TextField(**NULLABLE)

    def __str__(self):
        return f"{self.channel.upper()} to {self.notification.recipient} - {self.status}"

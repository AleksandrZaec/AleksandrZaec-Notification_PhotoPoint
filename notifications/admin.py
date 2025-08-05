from django.contrib import admin
from .models import DeliveryAttempt


@admin.register(DeliveryAttempt)
class DeliveryAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'notification', 'channel', 'status', 'sent_at')
    list_filter = ('channel', 'status', 'sent_at')
    search_fields = ('notification__recipient__email',
                     'notification__recipient__phone_number',
                     'error_message')
    readonly_fields = ('sent_at',)
    fieldsets = (
        (None, {
            'fields': ('notification', 'channel', 'status')
        }),
        ('Дополнительно', {
            'fields': ('sent_at', 'error_message'),
            'classes': ('collapse',)
        }),
    )

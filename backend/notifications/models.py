import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.timesince import timesince


class Notification(models.Model):
    NOTIFICATION_CHOICES = [
        ("NFR", "newfriendrequest"),
        ("AFR", "acceptedfriendrequest"),
        ("RFR", "rejectedfriendrequest"),
        ("POST_LIKE", "postlike"),
        ("POST_COMMENT", "postcomment")
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.CharField(max_length=250)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   related_name='created_notifications',
                                   on_delete=models.CASCADE)
    created_for = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name='received_notifications',
                                    on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=30,
                                         choices=NOTIFICATION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def time_ago(self):
        return timesince(self.created_at)

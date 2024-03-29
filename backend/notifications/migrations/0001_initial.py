# Generated by Django 4.2.7 on 2024-01-29 10:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("message", models.CharField(max_length=250)),
                (
                    "notification_type",
                    models.CharField(
                        choices=[
                            ("NFR", "newfriendrequest"),
                            ("AFR", "acceptedfriendrequest"),
                            ("RFR", "rejectedfriendrequest"),
                            ("POST_LIKE", "postlike"),
                            ("POST_COMMENT", "postcomment"),
                        ],
                        max_length=30,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_read", models.BooleanField(default=False)),
                ("object_id", models.PositiveIntegerField()),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="created_notifications",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "created_for",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="received_notifications",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at",),
                "indexes": [
                    models.Index(
                        fields=["content_type", "object_id"],
                        name="notificatio_content_702c56_idx",
                    )
                ],
            },
        ),
    ]

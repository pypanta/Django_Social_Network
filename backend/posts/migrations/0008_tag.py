# Generated by Django 4.2.7 on 2023-12-12 11:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0007_alter_comment_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
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
                ("name", models.CharField(max_length=50, unique=True)),
                ("posts", models.ManyToManyField(blank=True, to="posts.post")),
            ],
        ),
    ]

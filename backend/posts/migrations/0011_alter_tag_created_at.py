# Generated by Django 4.2.7 on 2024-01-09 07:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0010_tag_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tag",
            name="created_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]

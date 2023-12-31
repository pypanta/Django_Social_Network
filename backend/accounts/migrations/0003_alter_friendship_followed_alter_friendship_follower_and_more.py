# Generated by Django 4.2.3 on 2023-08-02 13:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_friendship_user_friendships'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendship',
            name='followed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='friendship',
            name='follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='friendships',
            field=models.ManyToManyField(related_name='followed_by', through='accounts.Friendship', to=settings.AUTH_USER_MODEL),
        ),
    ]

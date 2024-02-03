from django.test import TestCase

from accounts.models import User

from ..models import Notification


class NotificationTestCase(TestCase):

    def test_create_notification(self):
        created_by = User.objects.create(email='test1@email.com',
                                         password='test1234')
        created_for = User.objects.create(email='test2@email.com',
                                          password='test1234')
        notification = Notification.objects.create(
            created_by=created_by,
            created_for=created_for,
            message=f"{created_by} sent you a friend request",
            notification_type='newfriendrequest',
            content_object=created_by)

        self.assertEqual(Notification.objects.count(), 1)
        self.assertEqual(notification.message,
                         'test1@email.com sent you a friend request')
        self.assertEqual(notification.content_object, created_by)
        self.assertEqual(notification.content_type.model, 'user')

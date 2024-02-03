from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User

from ..models import Notification


class NotificationAPITestCase(APITestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create(email='test1@email.com',
                                         username='user1')
        self.user1.set_password('test1234')
        self.user1.is_active = True
        self.user1.save()
        self.user2 = User.objects.create(email='test2@email.com',
                                         username='user2')
        self.user2.set_password('test1234')
        self.user2.is_active = True
        self.user2.save()

    def _login_user(self, user, password=None):
        """
        Log in a user by making a POST request to the login endpoint.

        Parameters:
        - user: User instance representing the user to be logged in.
        - password: (Optional) Password to be used for the login attempt.
          If not provided, a default password ('test1234') is used for testing
          purposes.

        Returns:
        - Response: The HTTP response received after attempting to log in the
          user.

        Example:
        response = _login_user(user_instance, password='custom_password')
        """
        url = reverse('accounts:login')
        payload = {'email': user.email, 'password': 'test1234'}
        response = self.client.post(url, payload, format='json')
        return response

    def _create_notification(self, sender, recipient, message,
                             notification_type, content_object):
        """
        Create a new notification.

        Parameters:
            - sender: The sender of the notification (User instance).
            - recipient: The recipient of the notification (User instance).
            - message: The content of the notification message (str).
            - notification_type: The type of notification (str).
            - content_object: The related object for the notification
            (typically a model instance).
        Returns:
            - Notification: The newly created Notification instance.
        """
        return Notification.objects.create(
            created_by=sender,
            created_for=recipient,
            message=message,
            notification_type=notification_type,
            content_object=content_object)

    def test_get_user_notifications(self):
        self._create_notification(self.user1,
                                  self.user2,
                                  f"{self.user1} liked one of your posts",
                                  'postlike',
                                  self.user1)

        self._create_notification(self.user1,
                                  self.user2,
                                  f"{self.user1} commented one of your posts",
                                  'postlike',
                                  self.user1)

        self._login_user(self.user2)

        url = reverse('notifications:notifications')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['message'],
                         f"{self.user1} commented one of your posts")
        self.assertEqual(response.data[1]['message'],
                         f"{self.user1} liked one of your posts")

    def test_delete_single_user_notification(self):
        notification = self._create_notification(
            self.user1,
            self.user2,
            f"{self.user1} liked one of your posts",
            'postlike',
            self.user1)

        self._login_user(self.user2)
        url = reverse('notifications:notifications')
        payload = {'id': notification.id}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['message'],
                         'Notification successfully deleted!')

    def test_delete_all_user_notifications(self):
        self._create_notification(self.user1,
                                  self.user2,
                                  f"{self.user1} liked one of your posts",
                                  'postlike',
                                  self.user1)

        self._create_notification(self.user1,
                                  self.user2,
                                  f"{self.user1} commented one of your posts",
                                  'postlike',
                                  self.user1)

        self._login_user(self.user2)
        url = reverse('notifications:notifications')
        payload = {'all': True}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['message'],
                         'Notifications successfully deleted!')

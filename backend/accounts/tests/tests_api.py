from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from ..models import User


class AccountAPITestCase(APITestCase):
    def setUp(self):
        u = User.objects.create(email='test@email.com')
        u.set_password('test1234')
        u.save()

    def _login(self):
        url = reverse('login')
        payload = {'email': 'test@email.com', 'password': 'test1234'}
        response = self.client.post(url, payload, format='json')
        return response

    def test_signup_view(self):
        url = reverse('signup')
        payload = {
            'email': 'test2@email.com',
            'password': 'test1234',
            'password_confirm': 'test1234'
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(
            User.objects.get(email=payload['email']).email, 'test2@email.com'
        )

    def test_login_view(self):
        response = self._login()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data.keys())

    def test_logout_view(self):
        url = reverse('logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'You are now logged out!')

    def test_refresh_token_view(self):
        self._login()
        url = reverse('token_refresh')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data.keys())
        self.assertIn('refresh', response.data.keys())

    def test_user_api_view(self):
        self._login()
        url = reverse('user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@email.com')

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
        url = reverse('accounts:login')
        payload = {'email': 'test@email.com', 'password': 'test1234'}
        response = self.client.post(url, payload, format='json')
        return response

    def _create_user(self, count=0):
        users = []
        for i in range(1, count+1):
            users.append(
                User(username=f"user{i}", email=f"user{i}@email.com")
            )
        User.objects.bulk_create(users)

    def test_signup_view(self):
        url = reverse('accounts:signup')
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
        url = reverse('accounts:logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'You are now logged out!')

    def test_refresh_token_view(self):
        self._login()
        url = reverse('accounts:token_refresh')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data.keys())
        self.assertIn('refresh', response.data.keys())

    def test_user_api_view(self):
        self._login()
        url = reverse('accounts:user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@email.com')

    def test_user_search_api_view(self):
        self._login()
        self._create_user(4)
        url = reverse('accounts:search')
        query = url + '?q=user2'
        response = self.client.get(query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_user_searchand_ordering_ASC__api_view(self):
        self._login()
        self._create_user(4)
        url = reverse('accounts:search')
        query = url + '?q=user&ordering=username'
        response = self.client.get(query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(
            [u['username'] for u in response.data],
            ['user1', 'user2', 'user3', 'user4']
        )

    def test_user_searchand_ordering_DESC__api_view(self):
        self._login()
        self._create_user(4)
        url = reverse('accounts:search')
        query = url + '?q=user&ordering=-username'
        response = self.client.get(query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(
            [u['username'] for u in response.data],
            ['user4', 'user3', 'user2', 'user1']
        )

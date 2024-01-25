from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from ..models import User


class AccountAPITestCase(APITestCase):
    def setUp(self):
        u = User.objects.create(email='test@email.com')
        u.set_password('test1234')
        u.save()

    def _login(self, email='test@email.com', password='test1234'):
        url = reverse('accounts:login')
        payload = {'email': email, 'password': password}
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

    def test_follow_user_api_view(self):
        self._login()
        self._create_user(1)
        u1 = User.objects.filter(email__icontains='test').first()
        u2 = User.objects.filter(email__icontains='user').first()
        url = reverse('accounts:follow')
        payload = {'id': u2.id}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(u1.following.count(), 1)
        self.assertEqual(u2.followers.count(), 1)

    def test_unfollow_user_api_view(self):
        self._login()
        self._create_user(1)
        u1 = User.objects.filter(email__icontains='test').first()
        u2 = User.objects.filter(email__icontains='user').first()
        u1.follow(u2)
        self.assertEqual(u1.following.count(), 1)
        self.assertEqual(u1.following.first().followed, u2)
        url = reverse('accounts:unfollow')
        payload = {'id': u2.id}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(u1.following.count(), 0)

    def test_accept_friendship_api_view(self):
        self._login()
        self._create_user(1)
        u1 = User.objects.filter(email__icontains='test').first()
        u2 = User.objects.filter(email__icontains='user').first()
        u2.follow(u1)
        self.assertEqual(u1.followers.count(), 1)
        self.assertEqual(
            u1.followers.filter(follower__id=u2.id).first().status, 'PE')
        url = reverse('accounts:accept')
        payload = {'id': u2.id, 'status': 'accept'}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            u1.followers.filter(follower__id=u2.id).first().status, 'AC')

    def test_edit_user_profile_api_view(self):
        user = User.objects.filter(email__icontains='test').first()
        self.assertEqual(user.username, None)
        self.assertEqual(user.first_name, None)
        self.assertEqual(user.last_name, None)

        self._login()
        url = reverse('accounts:edit-profile', args=[user.id])
        payload = {'first_name': 'Testing',
                   'last_name': 'User',
                   'username': 'test'}
        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_updated = User.objects.filter(email__icontains='test').first()
        self.assertEqual(user_updated.username, 'test')
        self.assertEqual(user_updated.first_name, 'Testing')
        self.assertEqual(user_updated.last_name, 'User')

    def test_user_can_edit_only_his_own_profile(self):
        self._create_user(1)
        user = User.objects.filter(email__icontains='user').first()

        # log in as a test user
        self._login()
        url = reverse('accounts:edit-profile', args=[user.id])
        payload = {'first_name': 'Testing',
                   'last_name': 'User',
                   'username': 'test'}
        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'][:],
                         'You do not have permission to edit this profile.')

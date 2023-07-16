from django.test import Client, TestCase

from accounts.models import User


class UserTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_user(self):
        user = User.objects.create_user(email='test@email.com',
                                        password='test1234',
                                        username='test')
        self.assertEqual(user.email, 'test@email.com')
        self.assertEqual(user.username, 'test')
        self.assertTrue(user.check_password('test1234'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        # Test login user with a e-mail
        self.assertTrue(self.client.login(email='test@email.com',
                                          password='test1234'))
        # Test login user with a username
        self.assertTrue(self.client.login(username='test',
                                          password='test1234'))

    def test_create_user_with_email_only(self):
        user = User.objects.create_user(email='test@mail.com',
                                        password='test1234')
        self.assertFalse(user.username)

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(email='admin@email.com',
                                                  password='admin1234',
                                                  username='admin')
        self.assertEqual(superuser.email, 'admin@email.com')
        self.assertEqual(superuser.username, 'admin')
        self.assertTrue(superuser.check_password('admin1234'))
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_admin)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        # Test login superuser with e-mail
        self.assertTrue(self.client.login(email='admin@email.com',
                                          password='admin1234'))
        # Test login superuser with username
        self.assertTrue(self.client.login(username='admin',
                                          password='admin1234'))

    def test_create_superuser_with_email_only(self):
        user = User.objects.create_user(email='admin@mail.com',
                                        password='admin1234')
        self.assertFalse(user.username)

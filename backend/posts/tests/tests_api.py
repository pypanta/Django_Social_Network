from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User


class PostAPITestCase(APITestCase):
    def setUp(self):
        u = User.objects.create(email='test@email.com')
        u.set_password('test1234')
        u.save()

        url = reverse('login')
        payload = {'email': 'test@email.com', 'password': 'test1234'}
        self.client.post(url, payload, format='json')

    def test_post_list_view(self):
        url = reverse('posts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_create_view(self):
        url = reverse('posts')
        payload = {'body': 'Test post'}
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['body'], 'Test post')
        self.assertEqual(len(response.json()['post_images']), 0)

    def test_post_create_with_image_view(self):
        url = reverse('posts')
        payload = {
            'body': 'Test post with image',
            'images': SimpleUploadedFile(name='test_image.jpg',
                                         content=b'',
                                         content_type='image/jpeg')
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['body'], 'Test post with image')
        self.assertEqual(len(response.json()['post_images']), 1)

    def test_post_create_with_multiple_images_view(self):
        url = reverse('posts')
        images = [
            SimpleUploadedFile(name=f"image_{i}.jpg",
                               content=b'',
                               content_type='image/jpeg')
            for i in range(4)
        ]
        payload = {
            'body': 'Test post with image',
            'images': images
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['body'], 'Test post with image')
        self.assertEqual(len(response.json()['post_images']), 4)

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User

from ..models import Post


class PostAPITestCase(APITestCase):
    def setUp(self):
        u = User.objects.create(email='test@email.com')
        u.set_password('test1234')
        u.save()

        url = reverse('accounts:login')
        payload = {'email': 'test@email.com', 'password': 'test1234'}
        self.client.post(url, payload, format='json')

    def _create_posts(self, count=0):
        user = User.objects.first()
        posts = []
        for i in range(1, count+1):
            posts.append(Post(body=f"Test post {i}", created_by=user))
        Post.objects.bulk_create(posts)

    def test_post_list_view(self):
        url = reverse('posts:posts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_create_view(self):
        url = reverse('posts:posts')
        payload = {'body': 'Test post'}
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['body'], 'Test post')
        self.assertEqual(len(response.json()['post_images']), 0)

    def test_post_create_with_image_view(self):
        url = reverse('posts:posts')
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
        url = reverse('posts:posts')
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

    def test_user_post_list_view(self):
        self._create_posts(2)
        user = User.objects.first()
        url = reverse('posts:user_posts', args=[user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['posts']), 2)

    def test_post_search_api_view(self):
        self._create_posts(4)
        url = reverse('posts:search')
        query = url + '?q=post 2'
        response = self.client.get(query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_post_search_and_ordering_ASC_api_view(self):
        self._create_posts(4)
        url = reverse('posts:search')
        query = url + '?q=test post&ordering=body'
        response = self.client.get(query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(
            [p['body'] for p in response.data],
            ['Test post 1', 'Test post 2', 'Test post 3', 'Test post 4']
        )

    def test_post_search_and_ordering_DESC_api_view(self):
        self._create_posts(4)
        url = reverse('posts:search')
        query = url + '?q=test post&ordering=-body'
        response = self.client.get(query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(
            [p['body'] for p in response.data],
            ['Test post 4', 'Test post 3', 'Test post 2', 'Test post 1']
        )
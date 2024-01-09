from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User

from ..models import Comment, Post, Tag


class PostAPITestCase(APITestCase):
    def setUp(self):
        u = User.objects.create(email='test@email.com')
        u.set_password('test1234')
        u.save()

        url = reverse('accounts:login')
        payload = {'email': 'test@email.com', 'password': 'test1234'}
        self.client.post(url, payload, format='json')

    def _create_posts(self, count=0, user=None):
        if user is None:
            user = User.objects.first()

        posts = []
        for i in range(1, count+1):
            posts.append(Post(body=f"Test post {i}", created_by=user))
        Post.objects.bulk_create(posts)

    def _create_user(self, email=None, login=False):
        if email is None:
            email = 'test2@email.com'
        user = User.objects.create(email=email)
        user.set_password('test1234')
        user.save()
        if login:
            url = reverse('accounts:login')
            payload = {'email': email, 'password': 'test1234'}
            self.client.post(url, payload, format='json')
        return user

    def test_post_list_view(self):
        self._create_posts(count=5)
        url = reverse('posts:posts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

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
        self._create_posts(count=2)
        user = User.objects.first()
        url = reverse('posts:user_posts', args=[user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['posts']), 2)

    def test_post_search_api_view(self):
        self._create_posts(count=4)
        url = reverse('posts:search')
        query = url + '?q=post 2'
        response = self.client.get(query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_post_search_and_ordering_ASC_api_view(self):
        self._create_posts(count=4)
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
        self._create_posts(count=4)
        url = reverse('posts:search')
        query = url + '?q=test post&ordering=-body'
        response = self.client.get(query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(
            [p['body'] for p in response.data],
            ['Test post 4', 'Test post 3', 'Test post 2', 'Test post 1']
        )

    def test_post_like_view(self):
        self._create_posts(count=1)
        post = Post.objects.first()
        self.assertEqual(post.likes.count(), 0)
        self._create_user(login=True)
        url = reverse('posts:like', args=[post.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post.likes.count(), 1)
        self.assertEqual(response.data['message'], 'Liked')

    def test_post_unlike_view(self):
        self._create_posts(count=1)
        post = Post.objects.first()
        self._create_user(login=True)
        url = reverse('posts:like', args=[post.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post.likes.count(), 1)
        response_unlike = self.client.post(url)
        self.assertEqual(response_unlike.status_code, status.HTTP_200_OK)
        self.assertEqual(post.likes.count(), 0)
        self.assertEqual(response_unlike.data['message'], 'Unliked')

    def test_user_can_not_like_his_own_post(self):
        user = self._create_user(login=True)
        self._create_posts(count=1, user=user)
        post = Post.objects.first()
        self.assertEqual(post.likes.count(), 0)
        url = reverse('posts:like', args=[post.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post.likes.count(), 0)
        self.assertEqual(response.data['message'],
                         "You can't like your own post")

    def test_post_detail_api_view(self):
        self._create_posts(count=1)
        post = Post.objects.first()
        url = reverse('posts:post_detail', args=[post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'].replace('-', ''), post.id.hex)


class CommentAPITestCase(APITestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create(email='test@email.com')
        self.user.set_password('test1234')
        self.user.save()

        # Login user
        url = reverse('accounts:login')
        payload = {'email': self.user.email, 'password': 'test1234'}
        self.client.post(url, payload, format='json')

        # Create post
        self.post = Post.objects.create(body='Test post', created_by=self.user)

        # Create 5 comments
        for i in range(5):
             comment = Comment.objects.create(body=f"Test comment {i}",
                                              created_by=self.user)
             self.post.comments.add(comment)

    def test_comment_list_view(self):
        url = reverse('posts:comment', args=[self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_comment_create_view(self):
        url = reverse('posts:comment', args=[self.post.id])
        payload = {'body': 'Test comment'}
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['body'], 'Test comment')


class TagAPITestCase(APITestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create(email='test@email.com')
        self.user.set_password('test1234')
        self.user.save()

        # Login user
        url = reverse('accounts:login')
        payload = {'email': self.user.email, 'password': 'test1234'}
        self.client.post(url, payload, format='json')

        # Create tag
        self.tag = Tag.objects.create(name='test')

    def test_tag_list_api_view(self):
        url = reverse('posts:tags')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'test')
        self.assertEqual(len(response.data[0]['posts']), 0)

    def test_tag_detail_api_view(self):
        url = reverse('posts:tag-detail', args=[self.tag.name])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.tag.id))
        self.assertEqual(response.data['name'], 'test')

    def test_create_post_with_tags(self):
        url = reverse('posts:posts')
        payload = {'body': 'Test post with tags', 'tags': 'test,django,vuejs'}
        response = self.client.post(url, payload)
        post = Post.objects.get(id=response.data['id'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['body'], 'Test post with tags')
        self.assertEqual(Tag.objects.count(), 3)
        self.assertEqual(list(Tag.objects.all()), list(post.tags.all()))

import tempfile

from django.test import Client, TestCase

from accounts.models import User

from ..models import Comment, Post, PostImage


class PostModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@email.com',
                                        password='test1234')

    def test_create_post(self):
        post = Post.objects.create(body='Test post', created_by=self.user)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(post.body, 'Test post')


class PostImageModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@email.com',
                                        password='test1234')

    def test_create_post_image(self):
        post = Post.objects.create(body='Test post', created_by=self.user)
        image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        post_image = PostImage.objects.create(image=image, post=post)
        self.assertEqual(PostImage.objects.count(), 1)
        self.assertEqual(post.images.count(), 1)


class CommentModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@email.com',
                                        password='test1234')
        self.post = Post.objects.create(body='Test post',
                                        created_by=self.user)

    def test_create_comment(self):
        comment = Comment.objects.create(body='Test comment',
                                         created_by=self.user)
        self.post.comments.add(comment)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(comment.body, 'Test comment')
        self.assertEqual(self.post.comments.count(), 1)
        self.assertIn(comment, self.post.comments.all())

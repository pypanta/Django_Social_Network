from django.test import TestCase

from accounts.models import User
from notifications.utils import send_notification
from posts.models import Comment, Like, Post


class SendNotificationTestCase(TestCase):
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

    def test_send_notification_for_post_comment(self):
        post = Post.objects.create(body='Test post',
                                   created_by=self.user2)
        comment = Comment.objects.create(body='Test comment',
                                         created_by=self.user1)
        post.comments.add(comment)
        notification = send_notification(comment.created_by, post.created_by,
                                         'postcomment', post)
        self.assertEqual(notification.created_by, comment.created_by)
        self.assertEqual(notification.created_for, post.created_by)
        self.assertEqual(notification.content_object, post)
        self.assertEqual(notification.content_type.model, 'post')
        self.assertEqual(
            notification.message,
            f'{comment.created_by.username} commented one of your posts')

    def test_send_notification_for_post_like(self):
        post = Post.objects.create(body='Test post',
                                   created_by=self.user1)
        like = Like.objects.create(created_by=self.user2)
        post.likes.add(like)
        notification = send_notification(like.created_by, post.created_by,
                                         'postlike', post)
        self.assertEqual(notification.created_by, like.created_by)
        self.assertEqual(notification.created_for, post.created_by)
        self.assertEqual(notification.content_object, post)
        self.assertEqual(notification.content_type.model, 'post')
        self.assertEqual(
            notification.message,
            f'{like.created_by.username} liked one of your posts')

    def test_send_notification_for_friendship_request(self):
        follow, _ = self.user1.follow(self.user2)
        notification = send_notification(follow.follower, follow.followed,
                                         'newfriendrequest', follow.follower)
        self.assertEqual(notification.created_by, follow.follower)
        self.assertEqual(notification.created_for, follow.followed)
        self.assertEqual(notification.content_object, follow.follower)
        self.assertEqual(notification.content_type.model, 'user')
        self.assertEqual(
            notification.message,
            f'{follow.follower.username} sent you a friend request')

    def test_send_notification_for_accepted_friendship_request(self):
        follow, _ = self.user1.follow(self.user2)
        # Accept friendship
        follow.followed.followers.first().status = 'AC'
        notification = send_notification(follow.followed, follow.follower,
                                         'acceptedfriendrequest',
                                         follow.followed)
        self.assertEqual(notification.created_by, follow.followed)
        self.assertEqual(notification.created_for, follow.follower)
        self.assertEqual(notification.content_object, follow.followed)
        self.assertEqual(notification.content_type.model, 'user')
        self.assertEqual(notification.message,
                         f'{follow.followed.username} accepted friend request')

    def test_send_notification_for_rejected_friendship_request(self):
        follow, _ = self.user1.follow(self.user2)
        # Accept friendship
        follow.followed.followers.first().status = 'RE'
        notification = send_notification(follow.followed, follow.follower,
                                         'rejectedfriendrequest',
                                         follow.followed)
        self.assertEqual(notification.created_by, follow.followed)
        self.assertEqual(notification.created_for, follow.follower)
        self.assertEqual(notification.content_object, follow.followed)
        self.assertEqual(notification.content_type.model, 'user')
        self.assertEqual(notification.message,
                         f'{follow.followed.username} rejected friend request')

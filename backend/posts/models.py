import uuid

from django.conf import settings
from django.db import models
from django.utils.timesince import timesince


def upload_post_image(instance, filename):
    if instance.post.created_by.username:
        user = instance.post.created_by.username
    else:
        user = instance.post.created_by.email.split('@')[0]
    return f"post/{user}/{filename}"


class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   related_name='likes',
                                   on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   related_name='comments',
                                   on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   related_name='posts',
                                   on_delete=models.CASCADE)
    likes = models.ManyToManyField(Like, blank=True)
    comments = models.ManyToManyField(Comment, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.body:
            return self.body[:30]
        return ''

    class Meta:
        ordering = ('-created_at',)

    def post_images(self):
        return self.images.all()

    def time_ago(self):
        return timesince(self.created_at)


class PostImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=upload_post_image)
    post = models.ForeignKey(Post,
                             related_name='images',
                             on_delete=models.CASCADE)

    def __str__(self):
        if self.image:
            return self.image.url
        return ''

import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.db import models


def upload_user_avatar(instance, filename):
    if instance.username:
        user = instance.username
    else:
        user = instance.email.split('@')[0]
    return f"avatar/{user}/{filename}"


class UserManager(BaseUserManager):
    def create_user(self,
                    email,
                    password,
                    username=None,
                    first_name=None,
                    last_name=None):
        if not email:
            raise ValueError('User must have an email address')

        # if not username:
        #     raise ValueError('User must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)

        return user

    def create_superuser(self,
                         email,
                         password,
                         username=None):
        user = self.create_user(email, password, username)

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=30,
                                unique=True,
                                blank=True,
                                null=True)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to=upload_user_avatar,
                               blank=True,
                               null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    friendships = models.ManyToManyField('self',
                                         through='Friendship',
                                         symmetrical=False,
                                         related_name="followed_by")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return ''

    def follow(self, to_follow, status='PE'):
        if self == to_follow:
            return

        friendship, created = Friendship.objects.get_or_create(
            follower=self,
            followed=to_follow)

        return friendship, created

    def unfollow(self, to_unfollow):
        friendship = Friendship.objects.filter(follower=self,
                                               followed=to_unfollow)
        friendship_exists = friendship.exists()
        if friendship_exists:
            friendship.delete()

        return friendship_exists


class Friendship(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PE', 'Pending'
        ACCEPTED = 'AC', 'Accepted'
        REJECTED = 'RE', 'Rejected'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    follower = models.ForeignKey(User,
                                 related_name='following',
                                 on_delete=models.CASCADE)
    followed = models.ForeignKey(User,
                                 related_name='followers',
                                 on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.PENDING)

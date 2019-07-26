from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    full_name = models.CharField(max_length=100)
    avatar = models.CharField(max_length=100, null=True)
    verified_email = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True
    )
    @classmethod
    def get_user(cls, username=None, email=None):
        query = {}
        if username:
            query['username'] = username
        if email:
            query['email'] = email
        user = User.objects.filter(**query).first()
        return user

    @classmethod
    def add_user(cls, username, full_name, email):
        user = User(
            username=username,
            full_name=full_name,
            email=email
        )
        user.save()
        return user

    @classmethod
    def update(cls, user, data):
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            if user.email != data['email']:
                user.verified_email = False
            user.email = data['email']
        if 'fullname' in data:
            user.fullname = data['fullname']
        user.save()
        return user


class UserFollow(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower_user'
    )

    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following_user'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True
    )
    @classmethod
    def follow_user(cls, follower, following):
        user_follow = UserFollow.objects.filter(
            follower=follower,
            following=following
        ).first()
        if not user_follow:
            user_follow = UserFollow(
                follower=follower,
                following=following
            )
            user_follow.save()
        return user_follow

    @classmethod
    def unfollow_user(cls, follower, following):
        UserFollow.objects.filter(
            follower=follower,
            following=following
        ).delete()
        return True


class UserBlock(models.Model):
    blocker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blocker_user'
    )

    blocked = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blocked_user'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True
    )
    @classmethod
    def block_user(cls, blocker, blocked):
        user_block = UserBlock.objects.filter(
            blocker=blocker,
            blocked=blocked
        ).first()
        if not user_block:
            user_block = UserBlock(
                blocker=blocker,
                blocked=blocked
            )
            user_block.save()
        return user_block

    @classmethod
    def unblock_user(cls, blocker, blocked):
        UserBlock.objects.filter(
            blocker=blocker,
            blocked=blocked
        ).delete()
        return True

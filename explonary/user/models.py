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

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    objects = UserManager()

    def __str__(self):
        return self.username


class UserFollows(models.Model):
    user: CustomUser = models.ForeignKey(settings.AUTH_USER_MODEL,
                                         on_delete=models.CASCADE,
                                         related_name='following')

    followed_user: CustomUser = models.ForeignKey(settings.AUTH_USER_MODEL,
                                                  on_delete=models.CASCADE,
                                                  related_name='followed_by')

    class Meta:
        unique_together = ('user', 'followed_user')

    def __str__(self):
        return f"{self.user.username} follows {self.followed_user.username}"

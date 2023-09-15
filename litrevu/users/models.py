from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager


class CustomUser(AbstractUser):
    objects = UserManager()

    def __str__(self):
        return self.username

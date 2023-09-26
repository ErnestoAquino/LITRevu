from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator

from users.models import CustomUser


class Ticket(models.Model):
    title = models.fields.CharField(max_length = 128)
    description = models.fields.TextField(max_length = 2048, blank = True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    image = models.ImageField(null = True, blank = True)
    time_create = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title


class Review(models.Model):
    # ticket = models.ForeignKey(Ticket, on_delete = models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators = [MinValueValidator(0), MaxValueValidator(5)])
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    headline = models.CharField(max_length = 128)
    body = models.TextField(max_length = 8192, blank = True)
    time_create = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.headline

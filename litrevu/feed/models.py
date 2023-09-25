from django.db import models
from users.models import CustomUser


class Ticket(models.Model):
    title = models.fields.CharField(max_length = 128)
    description = models.fields.TextField(max_length = 2048, blank = True)

    image = models.ImageField(null = True, blank = True)
    time_create = models.DateTimeField(auto_now_add = True)


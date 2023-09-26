from django.contrib import admin
from users.models import CustomUser
from users.models import UserFollows

admin.site.register(CustomUser)
admin.site.register(UserFollows)

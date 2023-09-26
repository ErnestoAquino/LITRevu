from django.contrib import admin
from feed.models import Ticket
from feed.models import Review

admin.site.register(Ticket)
admin.site.register(Review)

from django.contrib import admin
from feed.models import Ticket
from feed.models import Review


class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('headline', 'ticket')


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)

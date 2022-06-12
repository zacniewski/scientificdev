from django.contrib import admin
from .models import Subscriber


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email_of_subscriber', 'status', 'saving_date')


admin.site.register(Subscriber, SubscriberAdmin)

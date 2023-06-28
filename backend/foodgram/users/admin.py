from django.contrib import admin

from .models import Subscription, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username')
    list_filter = ('email', 'username')


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)

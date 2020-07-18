from django.contrib import admin
from .models import Bot, UserLink

@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    fields = ['name', 'engine', 'token']
    list_display = ['name', 'engine', 'token']

@admin.register(UserLink)
class UserLinkAdmin(admin.ModelAdmin):
    fields = ['user', 'bot', 'chat_id', 'active']
    list_display = ['user', 'bot', 'chat_id', 'active']

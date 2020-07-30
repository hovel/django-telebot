from django.db import models
from telebot.base.models import UserLink
from . import FROM_BOT



class MessageLogRecord(models.Model):
    link = models.ForeignKey(UserLink, on_delete=models.DO_NOTHING)
    direction = models.SmallIntegerField(default=FROM_BOT)
    date = models.DateTimeField(db_index=True)
    message = models.TextField(default='')
    success = models.BooleanField(default=True)
    error = models.TextField(null=True)
    message_id = models.IntegerField(null=True)
    addional_info = models.CharField(max_length=500, null=True)

class SystemLogRecord(models.Model):
    link = models.ForeignKey(UserLink, on_delete=models.DO_NOTHING, null=True, blank=True)
    event_class = models.CharField(max_length=50, db_index=True)
    event = models.CharField(max_length=200)
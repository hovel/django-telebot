# Profile

from django.contrib.auth.models import User
from django.conf import settings
from telebot.engines import telegram
from django.db import models


REGISTRED_ENGINES_MODELS = {
    'telegram': telegram
}
#TODO Extend engines from settings

class Bot(models.Model):
    name = models.CharField(max_length=50, unique=True)
    engine = models.CharField(max_length=20)
    token = models.CharField(max_length=200, null=True, blank=True)


class UserLink(models.Model):
    user = models.OneToOneField(User)
    bot = models.OneToOneField(Bot)
    chat_id = models.CharField(max_length=100, db_index=True)
